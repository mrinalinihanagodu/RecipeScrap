# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3 as lite

con = None

class RefocusxPipeline(object):

    def __init__(self):
        self.setupDBCon()
        self.createTables()
        
    
    def process_item(self, item, spider):
        for key, value in item.iteritems():
	    if(isinstance(value, list)):
                if value:
		    templist = []
		    for obj in value:
			temp = self.stripHTML(obj)
			templist.append(temp)
			item[key] = templist
		else:
		    item[key] = ""
	    else:
		item[key] = self.stripHTML(value)
		
        self.storeInDB(item)
                
        return item

    def stripHTML(self, string):
	tagStripper = MLStripper()
	tagStripper.feed(string)
	return tagStripper.get_data()
               
    def storeInDB(self,item):
        self.storeRecipeInDb(item)

    def storeRecipeInDb(self,item):
        self.cur.execute("INSERT INTO Recipes(ingredients,recipe) VALUES(?,?)",(str(item.get('ingredients','')),str(item.get('recipe',''))))
        self.con.commit()

    def setupDBCon (self):
        self.con=lite.connect('test.db')
        self.cur = self.con.cursor()


    def __del__(self):
        self.closeDB()

    def createTables(self):

        self.dropRecipesTable()

        self.createRecipesTable()

    def createRecipesTable(self):
        self.cur.execute("CREATE TABLE IF NOT EXISTS Recipes(id INTEGER PRIMARY KEY NOT NULL, ingredients TEXT, recipe TEXT)")

    def dropRecipesTable(self):

        self.cur.execute("DROP TABLE IF EXISTS Recipes")

    def closeDB(self):
        self.con.close()

from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

