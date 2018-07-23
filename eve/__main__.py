#!/usr/bin/env python
# Copyright (c) 2015,2016, UT-BATTELLE, LLC
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
# 
# 3. Neither the name of the copyright holder nor the names of its contributors
# may be used to endorse or promote products derived from this software without
# specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from __future__ import absolute_import, division, print_function, unicode_literals

import os
import sys
import time
import argparse

import livvkit
from livvkit.util import options


def parse_args(args=None):
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-e', '--extensions',
                        action='store',
                        nargs='+',
                        default=None,
                        help='Specify the location of the JSON configuration files for the extended V&V tests to run.')
  
    parser.add_argument('-o', '--out-dir',
                        default=os.path.join(os.getcwd(), "vv_" + time.strftime("%Y-%m-%d")),
                        help='Location to output the EVE webpages.')
    
    args = parser.parse_args(args)
 
    options.parse_args(['-V']+args.extensions + ['-o', args.out_dir])
    
    from eve import resources 
    args.livv_resource_dir = livvkit.resource_dir
    livvkit.resource_dir = os.sep.join(resources.__path__)
    
    return args 


def main(cl_args=None):
    """ Direct execution. """

    if len(sys.argv) > 1:
        cl_args = sys.argv[1:]
    args = parse_args(cl_args)

    print("--------------------------------------------------------------------")
    print("                    ______  ____    ____  ______                    ") 
    print("                   |  ____| \ \ \  / / / |  ____|                   ")
    print("                   | |__     \ \ \/ / /  | |__                      ")
    print("                   |  __|     \ \/ / /   |  __|                     ")
    print("                   | |____     \  / /    | |____                    ")
    print("                   |______|     \/_/     |______|                   ")
    print("                                                                    ")
    print("    Extended Verification and Validation for Earth System Models    ")
    print("--------------------------------------------------------------------")
    print("\n  Current run: " + livvkit.timestamp)
    print(  "  User: "        + livvkit.user)
    print(  "  OS Type: "     + livvkit.os_type)
    print(  "  Machine: "     + livvkit.machine)
    print(  "  "              + livvkit.comment)

    from livvkit.components import validation
    from livvkit import scheduler
    from livvkit.util import functions
    from livvkit.util import elements
    
    functions.setup_output(jsd=os.path.join(args.livv_resource_dir, 'js'))
    
    l = []
    validation_config = {}
    print(" -----------------------------------------------------------------")
    print("   Beginning extensions test suite ")
    print(" -----------------------------------------------------------------")
    print("")
    for conf in livvkit.validation_model_configs:
        validation_config = functions.merge_dicts(validation_config, 
                                                  functions.read_json(conf))
    l.extend(scheduler.run_quiet(validation, validation_config,
                                 group=False))
    print(" -----------------------------------------------------------------")
    print("   Extensions test suite complete ")
    print(" -----------------------------------------------------------------")
    print("")
    
    result = elements.page("Summary", "", element_list=l)
    functions.write_json(result, livvkit.output_dir, "index.json")
    print("-------------------------------------------------------------------")
    print(" Done!  Results can be seen in a web browser at:")
    print("   " + os.path.join(livvkit.output_dir, 'index.html'))
    print("-------------------------------------------------------------------")


if __name__ == '__main__':
    main()