import os
import re
import csv
import sys
import resource
from pprint import pprint


class FileStreamer:
    BUFFER_SIZE = 1024 * 2     # in KB
    BUFFER_LINES = 2


    def __init__(self, file_path, allow_buffer_overflow = False):
        self.file_path = file_path
        self.file = None
        self.buffer = ""
        self.buffer_lines = 0
        self.allow_buffer_overflow = allow_buffer_overflow
        self.gen = None


    def open_file(self):
        try:
            self.file = open(self.file_path, "r")
            # print("File opened successfully.")
        except FileNotFoundError:
            # print("File not found.")
            pass
        except IOError:
            # print("Error opening the file.")
            pass


    def close_file(self):
        if self.file is not None:
            self.file.close()
            self.file = None
            # print("File closed.")
        else:
            # print("No file is currently open.")
            pass


    def read_line(self):
        if self.file is None:
            self.open_file()
        
        with self.file as file:
            for line in file:
                yield line
    

    def should_load_buffer(self):
        if self.allow_buffer_overflow:
            return True
        # if sys.getsizeof( self.buffer ) <= self.BUFFER_SIZE or self.buffer_lines <= self.BUFFER_LINES:
        if sys.getsizeof( self.buffer ) <= self.BUFFER_SIZE:
            return True
        return False


    def load_buffer(self):
        # print("inside load buffer")

        if self.gen is None:
            self.gen = self.read_line()

            # print("inside load buffer - gen created")
        
        while self.should_load_buffer():

            # print("inside load buffer - should_load_buffer: " + str(self.should_load_buffer()))

            try:
                line = next(self.gen)
                self.buffer = self.buffer + line
            except StopIteration:
                # closing file when no line
                self.close_file()
                return


    def read_buffer(self):
        # print("inside read buffer")

        self.load_buffer()
        return self.buffer


    def write_buffer(self, buffer):
        self.buffer = buffer


    def file_read_complete(self):
        # if file open -> not complete -> False
        if self.file:
            return False
        else:
            return True



class CSVInspector(FileStreamer):
    def __init__(self, file_path, allow_buffer_overflow = False, sep = ',', quote = '"', hasHeaders = True, comment = "#"):
        super().__init__(file_path, allow_buffer_overflow)
        self.sep = sep
        self.quote = quote
        self.hasHeaders = hasHeaders
        self.comment = comment

        self.skip = True
        self.formatAlways = True
        self.formatUnquoted = True

        self.regexQuote = re.compile(f'^{quote}([\\S\\s]*){quote}$')
        self.regexDoubleQuote = re.compile(f'{quote}{quote}', re.MULTILINE)
        self.regexComment = re.compile(fr'^\s*{re.escape(comment)}|^\s+$')

        self.regexLines = re.compile(f'(({quote}(?:[^{quote}]|)+{quote}|[^{quote}\n\r]+)+)', re.MULTILINE)

        self.regexItems = re.compile(f'{sep}(?=(?:[^{quote}]*{quote}[^{quote}]*{quote})*[^{quote}]*$)')

        self.headers = []
        self.firstLine = hasHeaders
        self.headersLen = 0




    def unquote(self, cell):
        quote = self.quote
        if len(cell["text"]) > 0:
            match = re.match(f'^{quote}([\\S\\s]*){quote}$', cell["text"])
            if match:
                cell["quoted"] = True
                return self.dblquote(match[1])
        return cell["text"]


    def dblquote(self, text):
        quote = self.quote
        return text.replace(f"{quote}{quote}", quote) if len(text) > 1 else text


    def isComment(self, text, skip, comment):
        if not skip:
            return False
        else:
            if len(text) > 0:
                return re.match(f'^\\s*{comment}|^\\s+$', text)
            else:
                return True


    # considers that some metadata is present in 1st row
    def isSep(self, text, sep, regexItems):
        quote = self.quote
        line = text.replace(" ", "")
        left = line[:4].lower()
        result = (left == "sep=")
        if result and len(line) == 5:
            escapes = "+*?^$\.[]{}()|/"
            char = line[4]
            sep = "\\" + char if char in escapes else char
            regexItems = re.compile(f'{sep}(?=(?:[^{quote}]*{quote}[^{quote}]*{quote})*[^{quote}]*$)')
        return result


    # considered the headers are able to parse correctly and that they are correct
    def parseLine(self):
        text = self.read_buffer()

        # print("inside parseline:\n" + text)

        match = self.regexLines.search( text )

        if match:
            currRawLine = match.group()

            newText = text[match.end():]

            self.write_buffer( newText )

            # count here is plausible  count of line match
            _, count = self.regexLines.subn("", newText) 
            
            line = currRawLine.replace("\r", "")
            # if i == 0 and self.isSep(line, self.sep, self.regexItems):
            #     continue

            if not self.isComment(line, self.skip, self.comment):
                items = self.regexItems.split(line)

                    # if len(items) > maxLength:
                    #     maxLength = len(items)

                if self.firstLine:
                    for item in items:
                        cell = {"text": item}
                        self.headers.append(self.unquote(cell))
                
                    self.headersLen = len(self.headers)
                    self.firstLine = False

                    with open(log, "a") as f:
                        # f.write(",".join(self.headers))
                        # f.write("\n")

                        # f.write(str(self.headers))
                        # f.write("\n")

                        writer = csv.writer(f)
                        writer.writerow(self.headers)

                    return self.headers, count

                else:
                    obj = []
                    for item in items:
                        cell = {"text": item, "quoted": False}
                        value = self.unquote(cell)
                        obj.append(value)

                    # if len(line) > 0 or (i < len(lines) - 1):
                    # if there's a blank line inbetween data then check if lines are present after it or not
                    if len(line) > 0 or ( not self.file_read_complete or count ):
                        if len(obj) == self.headersLen:

                            with open(log, "a") as f:
                                # f.write(",".join(obj))
                                # f.write(",".join([str(i) for i in obj]))
                                # f.write("\n")

                                # f.write(str(obj))
                                # f.write("\n")
                                
                                writer = csv.writer(f)
                                writer.writerow(obj)

                                pass

                    return obj, count
        return [], 0


    def parse(self):
        while True:
            row, count = self.parseLine()
            
            print(row, self.file_read_complete(), count)
            
            if not ( row or ( not self.file_read_complete() or count ) ):
                break





file_path = 'z_data_1.csv'
# file_path = 'inspect-multiline.csv'
# file_path = 'ItemMaster_MMS001.csv'
# file_path = 'z_data_4.csv'

global log

# log = "data.txt"
log = "test.csv"
# log = "data.csv"

# print(f'File Size is {os.stat(file_path).st_size / (1024 * 1024)} MB')


c = CSVInspector(file_path, sep='\t')

c.parse()




# print('Peak Memory Usage =', resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
# print('User Mode Time =', resource.getrusage(resource.RUSAGE_SELF).ru_utime)
# print('System Mode Time =', resource.getrusage(resource.RUSAGE_SELF).ru_stime)
