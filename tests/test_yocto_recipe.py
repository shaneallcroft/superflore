# Copyright 2017 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from time import gmtime, strftime
import re

from superflore.generators.bitbake.yocto_recipe import yoctoRecipe
import unittest

class TestYoctoRecipeOutput(unittest.TestCase):
    def get_yocto_recipe(self):
        yocto = yoctoRecipe()
        yocto.description = 'a yocto_recipe'
        yocto.author = 'author'
        yocto.src_uri = 'https://www.website.com/download/foo/archive/foo/release/lunar/0.0.0.tar.gz'
        yocto.name = 'foo-bar'
        #yocto.distro = 'lunar'   does open embedded want this?
        return yocto

    def test_simple(self):
        """Test Yocto Format"""
        yocto = self.get_yocto_recipe()
        yocto.add_depend('p2os_driver')  #did not know which depend to add, so I mirrored test_ebuild, probs is wrong
        got_text = yocto.get_recipe_text('Open Source Robotics Foundation', 'BSD')
        with open('tests/bitbake/simple_expected.bitbake', 'r') as expect_file:
            s = expect_file.read()
            correct_text = re.sub('Copyright 2017', 'Copyright ' + strftime("%Y", gmtime()), s)
        self.assertEqual(got_text, correct_text)

    def test_get_folder_name(self):
        """Test getFolderName"""
        yocto = self.get_yocto_recipe()
        got_folder_name = yocto.getFolderName()
        expected_folder_name = 'foo_bar-' + str(yocto.version)  #this probs wont work if the distro is supposed to be explicitly set in get_yocto_recipe
        self.assertEqual(got_folder_name, expected_folder_name)

    def test_get_archive(self):
        """Test getArchiveName"""
        yocto = self.get_yocto_recipe()
        got_archive_name = yocto.getArchiveName()
        expected_archive_name = yocto.tar_dir + "/" \
            + 'foo_bar' + '-' + str(yocto.version) \
            + '-' + yocto.distro + '.tar.gz'
        self.assertEqual(got_archive_name, expected_archive_name)

    def test_get_license_line(self):
        """Test get_license_line method"""
        yocto = self.get_yocto_recipe()
        sample_xml = 'blah \nblah \nlicense BSD \nblah'
        yocto.pkg_xml = sample_xml.encode('utf-8')
        yocto.get_license_line()
        self.assertEqual(yocto.license_line, '3')

    def test_download_archive(self):
        """Test downloadArchive"""
        #not sure how to test this yet, but this is certainly not it
        yocto = self.get_yocto_recipe()
        yocto.downloadArchive()
        #TODO(shaneallcroft) finish this^

    def test_get_src_location(self):
        #I do not know what this function does
    
