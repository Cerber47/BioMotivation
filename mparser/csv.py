
class CSVPreparationManager:
    def __init__(self, path='output/', output='output/'):
        self.input_path = path
        self.output_path = output

    def gff_data_to_csv(self, filename):
        f_in, f_out = self._gff_csv_stream(filename)

        f_out.write("name,ID,chr,feature,strand,start,end")
        while True:
            newline = f_in.readline()
            if newline:
                if newline.startswith("#"):
                    continue
                newline = self._parse_line_to_csv_line(newline.replace("\n", ""))
                f_out.write("\n")
                f_out.write(newline)
            else:
                break

    def _gff_csv_stream(self, filename):
        try:
            f_in = open(self.input_path + filename + '.gff')
        except FileNotFoundError:
            raise FileNotFoundError(f"File {filename + '.gff'} not found in {self.input_path}")

        try:
            f_out = open(self.output_path + filename + '.csv', 'w')
        except:
            f_in.close()
            raise Exception("Something has gone wrong")

        return f_in, f_out

    def _parse_line_to_csv_line(self, line: str):
        data = line.split("\t")

        try:
            chromoname = data[0]
            basename = data[1]
            featurename = data[2]
            sequencestart = data[3]
            sequenceend = data[4]
            _ = data[5]
            strand = data[6]
            _ = data[7]
            details = data[8]

            gene_id, gene_name  = self._parse_gene_details(details)

        except IndexError:
            raise Exception("Wrong file format. Data lacking information")

        except ValueError:
            raise Exception("Wrong file format. Start and end must be convertable to integer")

        if strand != "+" and strand != "-":
            raise Exception(f"Wrong file format. Strand must be + or -, not {strand}")

        if not sequencestart.isnumeric() or not sequenceend.isnumeric():
            raise Exception(f"Wrong file format. Start and end must be numeric")

        return ",".join([gene_name, gene_id, chromoname, featurename, strand, sequencestart, sequenceend])

    def _parse_gene_details(self, details: str):
        pairs = details.split(";")
        data = {}

        for pair in pairs:
            if pair:
                key = pair.split("=")[0]
                value = pair.split("=")[1]
                if value[0] == ":":
                    value = value[1:]
                data[key] = value
        if "ID" not in data.keys() and "Name" not in data.keys():
            raise Exception("Wrong data format. A gene must provide name and id info")

        return data["ID"], data["Name"]