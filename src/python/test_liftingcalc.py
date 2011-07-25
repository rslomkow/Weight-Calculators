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

import unittest
import liftingcalc as lc

class KnownValues (unittest.TestCase):
  """KnownValues is the test case for fixed inputs and outputs"""

  known_values = {
    'loadCommandLine':[
      # no arguments returns a simple default
      [[],({'sort': 'total_load'}, [1], [1], [[16, [[16]]], [24, [[24]]], [32, [[32]]]])],
      # make sure you can reset search order, use ranges for sets, manually define load
      [['-o','weight_load','-s','1-2','-l','5,10'],({'sort': 'weight_load'}, [1,2], [1], [[16, [[16]]], [24, [[24]]], [32, [[32]]]])],
      # barbell mode simple
      [['-b','18'],({'sort': 'total_load'}, [1], [1], [[18, [[18]]]])],
      # barbell mode than one solution
      [['-b','18','-p','5,5,10','-s','2','-o','weight_load'],({'sort': 'weight_load'}, [2], [1], [[18, [[18]]], [28, [[18,5,5]]], [38, [[18,5,5,5,5],[18,10,10]]],[48, [[18,10,5,10,5]]],[58,[18,10,5,5,10,5,5]]])],
      # dumbell mode sensible
      [['-d','2.5','-r','2.5,5'],({'sort': 'total_load'}, [1], [5], [[5, [[2.5,2.5]]], [10, [[2.5,2.5,2.5,25]]], [25, [[2.5,5,5,2.5,5,5]]],[35, [[2.5,5,2.5,5,2.5,2.5,5,2.5,5,2.5]]]])],
      # test the load option
      [['-l','10-12'],({'sort': 'total_load'}, [1], [1], [[10, [[10]]], [11, [[11]]], [12, [[12]]]])],
      ],
    'barbellOptions':[
      ],
    'dumbellOptions':[
      ],
    'weightLoadOptions':[
      ],
    'simpleLoadOptions':[
      ['5,10',[[5,[5]],[10,[10]]]],
      [['2-3'],[[2,[2]],[3,[3]]]],
      ],
    'parseNumbers':[
      ['1,5,7',True,[1,5,7]],
      ['1-3,7',True,[1,2,3,7]],
      ['2.5,5.5',False,[2.5,5.5]],
      ],
    }

  def testParseNumbers (self):
    """confirming that the parsing of numbers works"""
    for data in self.known_values['parseNumbers']:
      print "d:", data[0], data[1], data[2]
      result = lc.parseNumbers(data[0],integer=data[1])
      self.assertEqual(result,data[2])

  def testSimpleLoadOptions (self):
    """confirming we generate sane generic loads from plates"""
    for data in self.known_values['simpleLoadOptions']:
      print "d:", data[0], data[1]
      result = lc.simpleLoadOptions(data[0])
      self.assertEqual(result,data[1])

  def testLoadOptions (self):
    """confirming we generate sane generic loads from plates"""
    for data in self.known_values['weightLoadOptions']:
      print "d:", data[0], data[1]
      result = lc.weightLoadOptions(data[0])
      self.assertEqual(result,data[1])

  def testBarbellOptions (self):
    """confirming we generate sane barbell loads"""
    for data in self.known_values['barbellOptions']:
      print "d:", data[0], data[1], data[2]
      result = lc.barbellOptions(data[0],data[1])
      self.assertEqual(result,data[2])

  def testDumbellOptions (self):
    """confirming we generate sane dumbell loads"""
    for data in self.known_values['dumbellOptions']:
      print "d:", data[0], data[1], data[2]
      result = lc.dumbellOptions(data[0],data[1])
      self.assertEqual(result,data[2])

  def testLoadCommandLine (self):
    """confirming that ability to command line functionality works"""
    for data in self.known_values['loadCommandLine']:
      print "d:", data[0], data[1]
      result = lc.loadCommandLine(args=data[0])
      self.assertEqual(result,data[1])

if __name__ == "__main__":
    unittest.main() 
