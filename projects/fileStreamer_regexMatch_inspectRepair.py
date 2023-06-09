import os
import re
import csv
import sys
import resource
from pprint import pprint


class FileStreamer:
    BUFFER_SIZE = 1024 * 102     # in KB
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

        if self.should_load_buffer():
            self.load_buffer()
        
        return self.buffer


    def write_buffer(self, idx):
        self.buffer = self.buffer[idx:]
        _, count = self.regexLines.subn("", self.buffer)
        return count


    def file_read_complete(self):
        # if file open -> not complete -> False
        if self.file:
            return False
        else:
            return True



class CSVInspector(FileStreamer):
    def __init__(self, file_path, allow_buffer_overflow = False, sep = ',', quote = '"', quoteEscChar = "\\", hasHeaders = True, comment = "#"):
        super().__init__(file_path, allow_buffer_overflow)
        self.sep = sep
        self.quote = quote
        self.quoteEscChar = quoteEscChar
        self.hasHeaders = hasHeaders
        self.comment = comment

        self.skip = True
        self.formatAlways = True
        self.formatUnquoted = True

        self.regexQuote = re.compile(f'^{quote}([\\S\\s]*){quote}$')
        self.regexDoubleQuote = re.compile(f'{quote}{quote}', re.MULTILINE)
        self.regexComment = re.compile(fr'^\s*{re.escape(comment)}|^\s+$')

        self.regexLines = re.compile(f'(({quote}(?:[^{quote}]|)+{quote}|[^{quote}\n\r]+)+)', re.MULTILINE)

        self.regexNewLines = re.compile(rf'.+', re.MULTILINE)

        self.regexItems = re.compile(f'{sep}(?=(?:[^{quote}]*{quote}[^{quote}]*{quote})*[^{quote}]*$)')

        self.headers = []
        self.prev_rows = []
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


    def data_writer(self, s):
        if not log:
            return 
        
        with open(log, "a") as f:
            # f.write(",".join(currRow))
            # f.write(",".join([str(i) for i in currRow]))
            # f.write("\n")

            # f.write(str(s))
            # f.write("\n")
            
            writer = csv.writer(f)
            writer.writerow(s)

    
    def parseItems(self, line):
        items = self.regexItems.split(line)
        return items


    def parseLine(self):
        text = self.read_buffer()

        match = self.regexLines.search( text )

        if match:
            line = match.group()            
            line = line.replace("\r", "")

            return line, match.end()
        
        return "", 0


    def parseNewLine(self):
        text = self.read_buffer()

        match = self.regexNewLines.search( text )

        if match:
            line = match.group()            
            line = line.replace("\r", "")

            return line, match.end()
        
        return "", 0


    # considered the headers are able to parse correctly and that they are correct
    def parseText(self):
        line, idx = self.parseLine()
        nline, nidx = self.parseNewLine()

        # print(line, idx)
        # print(nline, nidx)

        # i = input()
        i = "0"

        if i == "0":
            rawLine = line
            rawIdx = idx
        else:
            rawLine = nline
            rawIdx = nidx

        if not rawLine:
            return [], 0
        
        if self.isComment(rawLine, self.skip, self.comment):
            return [], 0

        if self.firstLine:
            items = self.parseItems(rawLine)
            for item in items:
                cell = {"text": item}
                self.headers.append(self.unquote(cell))
            
            self.headersLen = len(self.headers)
            self.firstLine = False
            count = self.write_buffer(rawIdx)
            self.data_writer(self.headers)
            return self.headers, count
        
        else:
            row = []
            items = self.parseItems(rawLine)
            for item in items:
                cell = {"text": item, "quoted": False}
                value = self.unquote(cell)
                row.append(value)

            count = self.write_buffer(rawIdx)

            if len(rawLine) > 0 or ( not self.file_read_complete or count ):
                if len(row) == self.headersLen:
                    # self.data_writer(row)
                    pass
                else:
                    pass


            self.data_writer(row)
                
            return row, count


    def parse(self):
        while True:
            row, count = self.parseText()
            
            # print(row, self.file_read_complete(), count, "\n")
            print(row, self.file_read_complete(), count)
            
            # input()
            if not ( row or ( not self.file_read_complete() or count ) ):
                break


global log
log = None


files = [
    # 'zz_abdul_inspect-multiline.csv',
    # 'zz_keshab_ItemMaster_MMS001.csv',
    # 'zz_shan_icsp_sample_2.csv',
    'zz_shan_peoplec.csv',
    # 'zz_shan_sample_csv_with_multiline_records.csv',
    # 'zz_shan_sample_csv_with_multiline_records.csv',
]


for f in files:
    print(f"Working on {f}.")
    
    log = f"{f}_"

    try:
        os.remove(log)
        input()
    except:
        pass

    input()
    c = CSVInspector(f)

    c.parse()



# print('Peak Memory Usage =', resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
# print('User Mode Time =', resource.getrusage(resource.RUSAGE_SELF).ru_utime)
# print('System Mode Time =', resource.getrusage(resource.RUSAGE_SELF).ru_stime)
