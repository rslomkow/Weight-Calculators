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

import string

def loadCommandLine (args=None):
  """returns modes, sets, reps, load_profiles,
  where:
    modes =
      sort=[total_load|set_load|rep_load|weight_load]
    sets = integer for how many grouping are done
    reps = integer for how many times a lift is done with that weight_load
    load_profiles = array of the load and the weight configurations to get there
  """
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
    load_profiles = barbellOptions(float(options.barbell_load),
      parseNumbers(options.plates_load))
  elif options.dumbell_load:
    load_profiles = dumbellOptions(float(options.dumbell_load),
      parseNumbers(options.plates_load))
  elif options.plates_load:
    load_profiles = weightLoadOptions(parseNumbers(options.plates_load))
  elif options.load_range:
    load_profiles = simpleLoadOptions(parseNumbers(options.load_range))

  return (modes, sets, reps, load_profiles)

def appendLoad (result, index, config):
  """This adds a config to the result in appropriate format"""
  load = sum(config)
  if load in index:
    result[index[load]][1].append(config)
  else:
    result.append([load,[config]])
    index[load] = len(result) - 1

def barbellOptions (bar,plates):
  """return the load options based on the bar, and series_of_plates,
  assume they all are symetric plates 2x what was given"""
  index = {}
  result = []
  result.append([bar,[[bar]]])
  for plate_config in plateConfigs(plates):
    bb_config = [bar] + 2*plate_config
    appendLoad(result,index,bb_config)
  return result

def dumbellOptions (bar,plates):
  """return the load options based on the bar, and series_of_plates,
  assume a pair of dumbells and symetric plates 4x what was given"""
  index = {}
  result = []
  result.append([2*bar,[2*[bar]]])
  for plate_config in plateConfigs(plates):
    db_config = 2*[bar] + 4*plate_config
    appendLoad(result,index,db_config)
  return result

def weightLoadOptions (weights):
  """returns the load options of just set of plates"""
  result = []
  index = {}
  for plate_config in plateConfigs(weights):
    appendLoad(result,index,plate_config)
  return result

def plateConfigs (plates):
  """returns and array of all possible permutations of weights,
  sorted from largest to smallest"""
  result = []
  n = 0
  while n < len(plates):
    remainder = list(plates)
    if len(remainder) > 0:
      plate = remainder.pop(n)
      for config in plateConfigs(remainder):
	plate_config = [plate] + config
	plate_config.sort(reverse=True)
        result.append(plate_config)
      result.append([plate])
    n += 1
  result.sort()
  return uniqueList(result)


def simpleLoadOptions (weights):
  """return the load options for non-addable weights in the form [[load1,[weight1],[load2,[weight2]]"""
  result = []
  for load in weights:
    result.append([load,[[load]]])
  return result

def parseNumbers (istring,integer=False):
   """take a number string and return an array,
   where , seperates descrete elements and - seperates integer ranges"""
   array = []
   if not istring or istring == None:
     return array
   astring = str(istring)
   for number in astring.split(','):
     if '-' in number:
       start, stop = number.split('-')
       array.extend(range(int(start),int(stop)+1))
     elif integer:
       array.append(int(number))
     else:
       array.append(float(number))
   return array

def uniqueList(seq):  
    """give it a list and it will return a list of unqiue elements,
    even if the elements themselves are lists."""
    noDupes = [] 
    [noDupes.append(i) for i in seq if not noDupes.count(i)] 
    return noDupes

# Main for script mode
if __name__ == "__main__":
  (config, sets, reps, load_profiles) = loadCommandLine()
  print (config, sets, reps, load_profiles)
