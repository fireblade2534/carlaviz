from conans import ConanFile
from conan.tools.cmake import CMakeToolchain, CMakeDeps, CMake, cmake_layout
from conan.tools.files import (
    apply_conandata_patches,
    rename,
    replace_in_file,
    export_conandata_patches,
)
import os
import shutil
import subprocess


class Carla(ConanFile):
    name = "carla"

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "build_tests": [True, False],
        "with_client": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
        "build_tests": False,
        "with_client": True,
    }

    # Sources are located in the same place as this recipe, copy them to the recipe
    exports_sources = (
        "cmake/*",
        "CMakeLists.txt",
    )

    carla_version = "0.9.16"

    def _configure_cmake(self) -> CMake:
        cmake = CMake(self)
        variables = {"CARLA_VERSION": self.carla_version}
        if self.options.with_client:
            variables["CARLA_BUILD_CLIENT"] = "ON"
        cmake.configure(variables=variables)
        return cmake

    def _do_version_replace(self):
        # rename version file
        rename(
            self,
            os.path.join(
                self.source_folder, "LibCarla", "source", "carla", "Version.h.in"
            ),
            os.path.join(
                self.source_folder, "LibCarla", "source", "carla", "Version.h"
            ),
        )
        replace_in_file(
            self,
            os.path.join(
                self.source_folder, "LibCarla", "source", "carla", "Version.h"
            ),
            "${CARLA_VERSION}",
            f"{self.carla_version}",
        )

    def set_version(self):
        self.version = self.carla_version

    def requirements(self):
        self.requires("boost/1.84.0")
        self.requires("recastnavigation/carla_0.9.15")
        self.requires("rpclib/2.3.0")
        self.requires("libpng/1.6.37")
        if self.settings.os == "Windows":
            self.requires("zlib/1.2.13")
        if self.options.build_tests:
            self.requires("gtest/cci.20210126")

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def layout(self):
        cmake_layout(self)

    def source(self):
        # Sparse checkout avoids downloading CARLA's large documentation assets.
        upstream = os.path.join(self.source_folder, "_upstream")
        subprocess.run([
            "git", "clone", "--depth=1", "--filter=blob:none", "--sparse",
            "--branch", self.carla_version,
            "https://github.com/carla-simulator/carla.git", upstream,
        ], check=True)
        revision = subprocess.check_output(
            ["git", "-C", upstream, "rev-parse", "HEAD"], text=True
        ).strip()
        if revision != "294096eb1c38eabf246e4f3a9cdab704e33a7f4c":
            raise RuntimeError("Unexpected CARLA 0.9.16 source revision: " + revision)
        subprocess.run([
            "git", "-C", upstream, "sparse-checkout", "set", "LibCarla"
        ], check=True)
        shutil.move(os.path.join(upstream, "LibCarla"), self.source_folder)
        shutil.rmtree(upstream)

    def export_sources(self):
        export_conandata_patches(self)

    def generate(self):
        dp = CMakeDeps(self)
        dp.generate()
        tc = CMakeToolchain(self)
        tc.generate()

    def build(self):
        apply_conandata_patches(self)
        self._do_version_replace()
        cmake = self._configure_cmake()
        if self.should_build or self.should_test:
            cmake.build()
        if self.options.build_tests and self.should_test:
            if self.settings.os == "Windows":
                cmake.test()
            else:
                cmake.test(cli_args=["ARGS=-V"])

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["carla"]
        # We will use our installed cmake files
        self.cpp_info.set_property("cmake_find_mode", "none")
        self.cpp_info.builddirs.append(os.path.join("lib", "cmake", "carla"))
