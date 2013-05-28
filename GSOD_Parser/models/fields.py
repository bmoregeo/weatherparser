__author__ = 'christopherfricke'
import datetime
class Field():
    """
        Field
        This class defines a generic field type to be used by the weather reader
    """
    def __init__(self, field_length, name, null_value = None):
        """
        :param field_length: An value representing the length of the field in the GSOD table
        :type field_length: int
        :param name: Name of the field
        :type name: str
        :param null_value: A value that represents a null value in the table.
                            these will be replaced with None
        :type null_value: str, int, float
        :return:
        """
        self.length = field_length
        self.name = name
        self.null_value = null_value

    def parse(self, value):
        """
        Strips and returns a properly formatted value is not null or specified as a null value
        :param value: Field value to parse
        :type value: str
        :return:
        """
        if not value == self.null_value:
            return value.strip()
        else:
            return None

class CharField(Field):
    """
        String Field
        This class defines an string field type to be used by the weather reader
    """
    def parse(self, value):
        """
        Strips and returns a properly formatted string is not null or specified as a null value
        :param value: Field value to parse
        :type value: str
        :return:
        """
        if not value == self.null_value:
            return str(value.strip())
        else:
            return None

class FloatField(Field):
    """
        Float Field
        This class defines a float field type to be used by the weather reader
    """
    def parse(self, value):
        """
        Strips and returns a float is not null or specified as a null value
        :param value: Field value to parse
        :type value: str
        :return:
        """
        out = value.strip()
        if not out or out == str(self.null_value):
            return None
        else:
            return float(out)

class IntField(Field):
    """
        Integer Field
        This class defines an integer field type to be used by the weather reader
    """
    def parse(self, value):
        """
        Strips and returns an integer is not null or specified as a null value
        :param value: Field value to parse
        :type value: str
        :return:
        """
        out = value.strip()
        if not out or out == str(self.null_value):
            return 0
        else:
            return int(out)

class DateField(Field):
    """
        Date Field
        This class defines a datetime field type to be used by the weather reader
    """
    def __init__(self, field_length, name, datetime_format_string, null_value = None):
        """
        :param field_length: An value representing the length of the field in the GSOD table
        :type field_length: int
        :param name: Name of the field
        :type name: str
        :param datetime_format_string: A strptime datetime format string
        :type datetime_format_string: str
        :param null_value: A value that represents a null value in the table.
                            these will be replaced with None
        :type null_value: str, int, float
        :return:
        """
        Field.__init__(self, field_length, name, null_value)
        self.datetime_format = datetime_format_string
        self.name = name
        self.null_value = null_value

    def parse(self, value):
        """
        Strips and returns a datetime if the value is not null or specified as a null value
        :param value: Field value to parse
        :type value: str
        :return:
        """
        if not value or value == self.null_value:
            return 0
        else:
            return datetime.datetime.strptime(value.strip(), self.datetime_format)