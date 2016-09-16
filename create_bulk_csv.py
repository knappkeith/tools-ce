import string
import random
import json
import csv


class BulkTestDataGenerator(object):
    """
    Path should look something like:
        ../tests/crm/data/${element}/${RESOURCE}_upload.csv

    Easiest way to do that is to require path as argument.
    But that means *args doesn't work for field gen.
    So, probably fields should be passed into init function as a list.
    Args for init (# of records, desired fields)
    Args for CSV are file path (data is provided by the init, obvs.)
    """

    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'

    def __init__(self, num_records, **data):
        """
        Class Initializer, generates the data

        data is form key='value' where
            key: is the name of the value to be used in the
                 CSV header and the JSON attribute name
                value: is the type of key, current available are; 'email',
                   'name', 'single_name', 'string', and 'integer'.  if
                   not one of those and it's not of type string it will be
                   ignored. If it is of type string, then it will be a hard
                   coded value.
        NOTE: for the key in data you can use a single _ to get a . and
              two _ (__) to get a _ for the name, this is for nested
        """
        self.csv_header = []
        self.json_template = {}
        for key, value in data.iteritems():
            key = self._format_key(key)
            self.csv_header.append(key)
            self.json_template[key] = value
        self.num_records = num_records
        self.data = self._create_bulk_data(
            num_records=self.num_records,
            template=self.json_template)

    def write_bulk_csv(self, file_path, **kwargs):
        """
        Writes the data to a csv passed by 'file_path'
        No validation of file name
        """
        with open(file_path, 'wb') as bulk_csv:
            bulk_writer = csv.writer(bulk_csv, **kwargs)

            # Write the header
            bulk_writer.writerow(self.csv_header)

            # Write each line in DATA
            for data_line in self.data:
                write_array = []
                for value in self.csv_header:
                    if value in data_line.keys():
                        write_array.append(data_line[value])
                    else:
                        write_array.append("")
                bulk_writer.writerow(write_array)

    def update(self, data_key, entries=0):
        if isinstance(entries, list):
            for entry in entries:
                try:
                    self.data[entry][data_key] = \
                        self._get_data(self.json_template[data_key])
                except:
                    pass

    @property
    def json(self):
        """
        Return the JSON Blob of the data
        """
        json_data = json.dumps(self.data)
        return json_data

    @property
    def _email(self):
        return "%s@robottest.com" % self._str_generator()

    @property
    def _name(self):
        return "%s %s. %s" % (
            self._single_name,
            self._str_generator(size=1, chars=string.ascii_uppercase),
            self._single_name)

    @property
    def _single_name(self):
        return "%s%s" % (
            self._str_generator(size=1, chars=string.ascii_uppercase),
            self._str_generator(chars=string.ascii_lowercase))

    @property
    def _string(self):
        return self._str_generator(size=12)

    @property
    def _integer(self):
        return self._str_generator(size=6, chars=string.digits)

    def _create_bulk_data(self, num_records, template):
        data = []
        for i in range(0, num_records):
            line_data = {}
            for key, value in template.iteritems():
                new_value = self._get_data(value)
                if new_value:
                    line_data[key] = new_value
            data.append(line_data)
        return data

    def _get_data(self, value):
        if value == "name":
            return self._name
        elif value == "single_name":
            return self._single_name
        elif value == "email":
            return self._email
        elif value == "string":
            return self._string
        elif value == "integer":
            return self._integer
        elif isinstance(value, str) or isinstance(value, unicode):
            return value

    def _str_generator(
            self,
            size=None,
            chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
        if not size:
            size = random.choice(range(4, 8))
        return ''.join(random.choice(chars) for _ in range(size))

    def _format_key(self, key):
        # This is the '_'=='.'/"__"=="_" version
        # First split by "__"
        a = key.split("__")
        for index, i in enumerate(a):
            a[index] = ".".join(i.split("_"))
        return "_".join(a)
        # This is the '__'=='.'/'_'=='_' version
        # return ".".join(key.split("__"))
