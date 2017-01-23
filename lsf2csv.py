#!/usr/bin/env python
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#    
#   This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import struct
import argparse


class LSF_Header(object):
    pass


def read_file(file_name):
    with open(file_name) as file:
        raw_data = file.read()
        
    delimiter = raw_data.index('#')
    
    raw_header = raw_data[:delimiter]
    count_len = int(raw_data[delimiter + 1])
    num_of_bytes = int(raw_data[delimiter + 2: delimiter + 2 + count_len])
    raw_byte_data = raw_data[delimiter + 2 + count_len:]
    int_data = struct.unpack('{}h'.format(num_of_bytes / 2), raw_byte_data)
    
    header = {}
    header_attrs = raw_header.split(';')
    
    for header_attr in header_attrs:
        try:
            key, value = header_attr.split(',')
        except ValueError:
            break
        header[key] = value
        
    data = [float(x) * float(header['Vertical Scale']) for x in int_data]
    
    return header, data
    
def main():
    parser = argparse.ArgumentParser(description = 'Convert LSF file to CSV')
    parser.add_argument('file_name', type=str, nargs='+', 
            help='LSF file to convert')
    args = parser.parse_args()
    
    
    for file in args.file_name:
    
        if not (file.endswith('.lsf') or file.endswith('.LSF')):
            raise RuntimeError

        new_file_name = '{}.csv'.format(file[:-4])
                    
        print 'Processing file {} to {}'.format(file, new_file_name)
        header, data = read_file(file)
        print '{} at {}, {} samples'.format(header['Source'], header['Time'], 
                header['Memory Length'])
        
        with open(new_file_name, 'w') as output:
            for num in data:
                output.write('{},\n'.format(num))

main()
