
class gffPreparationManager:
    def __init__(self, path='input/', output='output/'):
        self.path_to_input = path
        self.path_to_output = output

    def separate_fasta(self, filename):
        f_in, f_gff, f_fasta = self._open_gff_and_fasta(filename)

        fasta_flag = False
        first_flag = True
        while True:
            newline = f_in.readline()
            if newline:
                if "##FASTA" in newline:
                    fasta_flag = True
                    first_flag = True
                    continue
                if "###" in newline:
                    continue
                if fasta_flag:
                    if first_flag:
                        first_flag = False
                    else:
                        f_fasta.write("\n")
                    f_fasta.write(newline.replace("\n", ""))
                else:
                    if first_flag:
                        first_flag = False
                    else:
                        f_gff.write("\n")
                    f_gff.write(newline.replace("\n", ""))
            else:
                break

        f_in.close()
        f_gff.close()
        f_fasta.close()

    def _open_gff_and_fasta(self, filename: str):
        try:
            print(self.path_to_input + filename + ".gff")
            f_in = open(self.path_to_input + filename + ".gff", 'r')
        except FileNotFoundError:
            raise FileNotFoundError(f"File {filename + '.gff'} not found in {self.path_to_input}")

        try:
            f_out_gff = open(self.path_to_output + filename + "_data.gff", 'w')
            f_out_fasta = open(self.path_to_output + filename + "_fasta.fasta", 'w')
        except:
            f_in.close()
            raise Exception("Something has gone wrong")

        return f_in, f_out_gff, f_out_fasta
