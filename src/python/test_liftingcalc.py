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
      [['-o','weight_load','-s','1-2','-l','5,10'],({'sort': 'weight_load'}, [1,2], [1], [[5.0, [[5.0]]], [10.0, [[10.0]]]])],
      # barbell mode simple
      [['-b','18'],({'sort': 'total_load'}, [1], [1], [[18, [[18]]]])],
      # barbell mode than one solution
      [['-b','18','-p','5,5,10','-s','2','-o','weight_load'],({'sort': 'weight_load'}, [2], [1], [[18.0, [[18.0]]], [28.0, [[18.0,5.0,5.0]]], [38.0, [[18.0,5.0,5.0,5.0,5.0],[18.0,10.0,10.0]]],[48.0, [[18.0,10.0,5.0,10.0,5.0]]],[58.0,[[18.0,10.0,5.0,5.0,10.0,5.0,5.0]]]])],
      # dumbell mode sensible
      [['-d','2.5','-r','5','-p','2.5,5'],({'sort': 'total_load'}, [1], [5], [[5.0, [[2.5, 2.5]]], [15.0, [[2.5, 2.5, 2.5, 2.5, 2.5, 2.5]]], [25.0, [[2.5, 2.5, 5.0, 5.0, 5.0, 5.0]]], [35.0, [[2.5, 2.5, 5.0, 2.5, 5.0, 2.5, 5.0, 2.5, 5.0, 2.5]]]])],
      # test the load option
      [['-l','10-12'],({'sort': 'total_load'}, [1], [1], [[10, [[10]]], [11, [[11]]], [12, [[12]]]])],
      ],
    'barbellOptions':[
      [10,[],[[10,[[10]]]]],
      [10,[5],[[10,[[10]]],[20,[[10,5,5]]]]],
      [18,[10,5,5],[[18, [[18]]], [28, [[18,5,5]]], [38, [[18,5,5,5,5],[18,10,10]]],[48, [[18,10,5,10,5]]],[58,[[18,10,5,5,10,5,5]]]]],
      ],
    'dumbellOptions':[
      [2.5,[2.5,5],[[5.0,[[2.5,2.5]]],[15.0,[[2.5,2.5,2.5,2.5,2.5,2.5]]],[25.0,[[2.5,2.5,5,5,5,5]]],[35.0,[[2.5,2.5,5,2.5,5,2.5,5,2.5,5,2.5]]]]],
      ],
    'weightLoadOptions':[
      [[1],[[1,[[1]]]]],
      [[2,5],[[2,[[2]]],[5,[[5]]],[7,[[5,2]]]]],
      [[1,1,2],[[1,[[1]]],[2,[[1,1],[2]]],[3,[[2,1]]],[4,[[2,1,1]]]]],
      ],
    'simpleLoadOptions':[
      [[5,10],[[5,[[5]]],[10,[[10]]]]],
      [[2,3],[[2,[[2]]],[3,[[3]]]]],
      ],
    'parseNumbers':[
      ['1,5,7',True,[1,5,7]],
      ['1-3,7',True,[1,2,3,7]],
      ['2.5,5.5',False,[2.5,5.5]],
      ],
    'uniqueList':[
      [[1,2,2,3,3,3],[1,2,3]],
      [[3,2,3,1,3,2],[3,2,1]],
      [[[4,3],[1,2],[4,3]],[[4,3],[1,2]]],
      [[5,6,7],[5,6,7]],
      ],
    'plateConfigs':[
      [[0],[[0]]],
      [[1,2],[[1],[2],[2,1]]],
      [[3,3],[[3],[3,3]]],
      ],
    'appendLoad':[
      [[],{},[1],[[1,[[1]]]]],
      [[[1,[[1]]],[7,[[4,3]]]],{7:1,1:0},[4,4],[[1,[[1]]],[7,[[4,3]]],[8,[[4,4]]]]],
      [[[1,[[1]]],[7,[[4,3]]],[8,[[4,4]]]],{1:0,7:1,8:2},[6,2],[[1,[[1]]],[7,[[4,3]]],[8,[[4,4],[6,2]]]]],
      ],
    }

  def testAppendLoad (self):
    """making sure we can reuse appendLoad logic to add things to the load data-structure"""
    for data in self.known_values['appendLoad']:
      result = data[0]
      lc.appendLoad(result,data[1],data[2])
      self.assertEqual(result,data[3])
    
  def testUniqueList (self):
    """confirming a list of non-unique items returns a unique list,
    even when the list of lists"""
    for data in self.known_values['uniqueList']:
      result = lc.uniqueList(data[0])
      self.assertEqual(result,data[1])

  def testPlateConfigs (self):
    """test that we do generate all expected combinations of plates"""
    for data in self.known_values['plateConfigs']:
      result = lc.plateConfigs(data[0])
      self.assertEqual(result,data[1])

  def testParseNumbers (self):
    """confirming that the parsing of numbers works"""
    for data in self.known_values['parseNumbers']:
      result = lc.parseNumbers(data[0],integer=data[1])
      self.assertEqual(result,data[2])

  def testSimpleLoadOptions (self):
    """confirming we generate sane generic loads from plates"""
    for data in self.known_values['simpleLoadOptions']:
      result = lc.simpleLoadOptions(data[0])
      self.assertEqual(result,data[1])

  def testWeightLoadOptions (self):
    """confirming we generate sane generic loads from plates"""
    for data in self.known_values['weightLoadOptions']:
      result = lc.weightLoadOptions(data[0])
      self.assertEqual(result,data[1])

  def testBarbellOptions (self):
    """confirming we generate sane barbell loads"""
    for data in self.known_values['barbellOptions']:
      result = lc.barbellOptions(data[0],data[1])
      self.assertEqual(result,data[2])

  def testDumbellOptions (self):
    """confirming we generate sane dumbell loads"""
    for data in self.known_values['dumbellOptions']:
      result = lc.dumbellOptions(data[0],data[1])
      self.assertEqual(result,data[2])

  def testLoadCommandLine (self):
    """confirming that ability to command line functionality works"""
    for data in self.known_values['loadCommandLine']:
      result = lc.loadCommandLine(args=data[0])
      self.assertEqual(result,data[1])

if __name__ == "__main__":
    unittest.main() 
