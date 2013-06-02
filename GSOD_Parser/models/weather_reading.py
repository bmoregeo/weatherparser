__author__ = 'christopherfricke'
import fields
import struct
class weatherReading(object):
    """
        Weather Reading
        This class defines how to parse a record in a GSOD table
    """
    def __init__(self, row):
        """
        :param row: A record in a parsed text file
        :type row: list
        :return:
        """
        stationid = fields.CharField(12, 'station')
        date = fields.DateField(10, 'date', '%Y%m%d')
        temperature = fields.FloatField(8, 'avg_temperature', 9999.9)
        temp_count = fields.IntField(3, 'temp_count')
        dewp = fields.FloatField(8, 'dewpoint', 9999.9)
        dewp_count = fields.IntField(3, 'dewpoint_count')
        slp = fields.FloatField(8, 'sea_level_pressure', 9999.9)
        slp_count = fields.IntField(3, 'slp_count')
        stp = fields.FloatField(8, 'station_pressure', 9999.9)
        stp_count = fields.IntField(3, 'stp_count')
        visib = fields.FloatField(7, 'visibility', 999.9)
        visib_count = fields.IntField(3, 'visib_count')
        wdsp = fields.FloatField(7, 'windspeed', 999.9)
        wdsp_count = fields.IntField(3, 'wdsp_count')
        maxspd = fields.FloatField(7, 'max_windspeed', 999.9)
        gust = fields.FloatField(7, 'gust', 999.9)
        max = fields.FloatField(8, 'max_temperature', 9999.9)
        max_flag = fields.CharField(1, 'max_temp_flag')
        min =  fields.FloatField(7, 'min_temperature', 9999.9)
        min_flag = fields.CharField(1, 'min_temp_flag')
        prcp = fields.FloatField(6, 'total_precipitation', 99.99)
        prcp_flag = fields.CharField(1, 'precipitation_flag')
        sndp = fields.FloatField(6, 'snow_depth', 999.9)
        sndp_flag = fields.IntField(1, 'snow_depth_flag')
        fog = fields.IntField(1, 'fog')
        rain = fields.IntField(1, 'rain')
        snow = fields.IntField(1, 'snow')
        hail = fields.IntField(1, 'hail')
        thunder = fields.IntField(1, 'thunder')
        tornado = fields.IntField(1, 'tornado')

        self.field_list = (
            stationid,
            date,
            temperature,
            temp_count,
            dewp,
            dewp_count,
            slp,
            slp_count,
            stp,
            stp_count,
            visib ,
            visib_count,
            wdsp,
            wdsp_count,
            maxspd ,
            gust,
            max ,
            max_flag,
            min,
            min_flag,
            prcp,
            prcp_flag,
            sndp,
            sndp_flag ,
            fog,
            rain,
            snow,
            hail,
            thunder,
            tornado
        )
        self.row = row

    @property
    def __format_string(self):
        """
        Format string to use for the struct operation
        :return: A properly formatted struct formatted string
        """
        return ''.join('%ds' % f.length for f in self.field_list)

    @property
    def parsed(self):
        """
        Returns a parsed GSOD table record as a dictionary
        :return: parsed record
        """
        parser = struct.Struct(self.__format_string).unpack_from
        parsed_values = parser(self.row)

        return dict([(field.name,field.parse(parsed_values[x])) for  x, field in enumerate(self.field_list)])

