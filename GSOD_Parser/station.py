__author__ = 'christopherfricke'
import gzip
import os
import datetime
import pprint

import settings
from bson import json_util
from models import weather_reading
import utilities as u


class station(object):
    """
    """
    def __init__(self, station_file):
        """
        :param station_file: A gziped yearly weather station file
        :type station_file: gzip file
        :return:
        """
        self.file = station_file
        self.file_name = os.path.splitext(os.path.basename(self.file))[0]
        self.__formats = None
        self.__output_location = None
        self.__records = []


    @property
    def output_location(self):
        return self.__output_location

    @output_location.setter
    def output_location(self, directory):
        self.__output_location = directory

    @property
    def formats(self):
        return self.__formats

    @formats.setter
    def formats(self, formats):
        self.__formats = formats



    def unzip(self):
        """
        Unzips and loads records into a temp list

        :return:
        """
        u.make_message('\t\tUnzipping %s' % os.path.basename(self.file), 2)
        with gzip.open(self.file, 'rb') as f:
            f.next() # Skip first row

            # Load all records into a list

            for row in f:
                wr = weather_reading.weatherReading(row)
                self.__records.append(wr.parsed)

    def filter(self, timestamp):
        """
        If timestamp is specified then filter results

        :param timestamp: A date represented as a string in %Y-%m-%d format (YEAR-MO-DA)
        :type timestamp: str
        :return:
        """
        if timestamp:
            timestamp = datetime.datetime.strptime(timestamp, '%Y-%m-%d')
            self.__records = filter(lambda row: row['date'] >= timestamp, self.__records)

    def export_to_json(self):
        """
        Exports the records to a JSON formatted file.  Output file is in the output location + input file name + '.json'

        :return:
        """
        import json
        u.make_message('\t\tExporting to JSON %s' % os.path.basename(self.file))

        output = os.path.join(self.output_location, self.file_name + '.json')

        with open(output, 'w') as w:
            w.write(json.dumps(self.__records, default=json_util.default))
        del output

    def export_to_csv(self):
        """
        Exports the records to a CSV formatted file.  Output file is in the output location + input file name + '.csv'

        :return:
        """
        import csv
        u.make_message('\t\tExporting to JSON %s' % os.path.basename(self.file))

        output = os.path.join(self.output_location, self.file_name + '.csv')
        with open(output, 'w') as w:
            c = csv.DictWriter(w, self.__records[0].keys())
            c.writeheader()
            c.writerows(self.__records)
            del c
        del output

    def load_into_mongo(self):
        from pymongo import MongoClient
        client = MongoClient(settings.mongo_info['hostname'], settings.mongo_info['port'])
        db = client[settings.mongo_info['database']]
        collection = db[settings.mongo_info['collection']]
        collection.insert(self.__records)

        del collection
        del db
        del client

    def export(self):
        """
        Export records to one of the following formats:
            - Print: Just print to console
            - JSON: Write json to file
            - CSV: write to csv file
            - Mongo: Load into MongoDB

        :return:
        """
        if self.__records:
            if self.formats['print']:
                pp = pprint.PrettyPrinter(indent=4)
                pp.pprint(self.__records)

            if self.formats['json']:
                self.export_to_json()

            if self.formats['csv']:
                self.export_to_csv()

            if self.formats['mongo']:
                self.load_into_mongo()
        else:
            u.make_message('\t\tNo Records Exist!', 3)