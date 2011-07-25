#!/usr/bin/python
# 
# Copyright (C) 2011  Robin * Slomkowski
# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
# 
# for the full text: http://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# 

"""liftingcalc: is module/script for managing weights and progressions"""

def loadCommandLine (args=None):
  """returns modes, sets, reps, load_profiles,
  where:
    modes =
      sort=[total_load|set_load|rep_load|weight_load]
    sets = integer for how many grouping are done
    reps = integer for how many times a lift is done with that weight_load
    load_profiles = array of the load and the weight configurations to get there
  """
  import string
  from optparse import OptionParser
  sort_types = ('total_load','set_load','rep_load','weight_load')
  sort_types_string = '['+string.join(sort_types,'|')+']'

  # defaults to my KBs as singles
  load_profiles = [[16,[[16]]],[24,[[24]]],[32,[[32]]]]
  modes = {}

  parser = OptionParser()
  parser.add_option( "-l", "--load_range", dest="load_range",
    help="this is the weight loaded comma seperated")
  parser.add_option( "-b", "--barbell_load", dest="barbell_load",
    help="the load of the barbell bar, assuming 2 equal plates")
  parser.add_option( "-d", "--dumbell_load", dest="dumbell_load",
    help="the weight of the dumbell bar, assuming two 2 equal bars and 4 equal plates")
  parser.add_option( "-p", "--plates_load", dest="plates_load",
    help="this is the range of plates, assumes equal across both sides of barbell/dumbell comma seperated")
  parser.add_option( "-r", "--rep_range", dest="rep_range", default='1',
    help="this is the number of reps per set comma seperated or '-' for range")
  parser.add_option( "-s", "--set_range", dest="set_range", default='1',
    help="this is the sets pers workout comma seperated or '-' for range")
  parser.add_option( "-o", "--order", dest="sort_order", default='total_load',
    help="must be one of: "+sort_types_string)
  (options, parsed_args) = parser.parse_args(args=args)

  if options.sort_order in sort_types:
    modes['sort'] = options.sort_order
  else:
    parser.error("'"+options.sort_order+"' is not a valid argument to --order")

  reps = parseNumbers(options.rep_range,integer=True)
  sets = parseNumbers(options.set_range,integer=True)

  if options.barbell_load:
    load_profiles = barbellOptions()
  elif options.dumbell_load:
    load_profiles = dumbellOptions()
  elif options.plates_load:
    load_profiles = weightLoadOptions(options.plates_load)
  elif options.load_range:
    load_profiles = simpleLoadOptions(options.load_range)

  return (modes, sets, reps, load_profiles)

def barbellOptions (bar,plates):
  """return the load options based on the bar, and series_of_plates,
  assume they all are symetric plates 2x what was given"""
  result = []
  return result

def dumbellOptions (bar,plates):
  """return the load options based on the bar, and series_of_plates,
  assume a pair of dumbells and symetric plates 4x what was given"""
  result = []
  return result

def weightLoadOptions (weights):
  """return the load options based on series of addable weights"""
  result = []
  for load in parseNumbers(weights):
    result.append()
  return result

def simpleLoadOptions (weights):
  """return the load options for non-addable weights in the form [[load1,[weight1],[load2,[weight2]]"""
  result = []
  return result

def parseNumbers (string,integer=False):
   """take a number string and return an array,
   where , seperates descrete elements and - seperates integer ranges"""
   array = []
   if not string:
     return array
   for number in string.split(','):
     if '-' in number:
       start, stop = number.split('-')
       array.extend(range(int(start),int(stop)+1))
     elif integer:
       array.append(int(number))
     else:
       array.append(float(number))
   return array

# Main for script mode
if __name__ == "__main__":
  (modes, sets, reps, load_profiles) = loadCommandLine()
  print (modes, sets, reps, load_profiles)
