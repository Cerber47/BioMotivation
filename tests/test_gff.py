import pytest
import os

from mparser import gff

class Test_gffPreparationManager:

    def setup(self):
        print("SetUp")
        self.path = 'testgff/'
        self.module = gff.gffPreparationManager(path=self.path, output=self.path)
        self.files_to_remove = []
        self.streams_to_close = []

    def test_separate_fasta(self):
        filename = 'SampleSplit'
        print("Hello world")
        self.module.separate_fasta(filename)

        self.files_to_remove.append(self.path + "SampleSplit_data.gff")
        self.files_to_remove.append(self.path + "SampleSplit_fasta.fasta")

        with open(self.path + "SampleSplit_data.gff") as f:
            data_gff = f.read()

        expected_gff_data = """##gff-version 3
##sequence-region test 1 10
test testBase testFeature 1 10 . + . ID=testSeq1;Name=noname;"""

        with open(self.path + "SampleSplit_fasta.fasta") as f:
            data_fasta = f.read()

        expected_fasta_data = """>test
CAAAAAAAAT"""

        assert data_gff == expected_gff_data
        assert data_fasta == expected_fasta_data

    def test_open_gff_fasta(self):
        filename = "testFile"

        f_1, f_2, f_3 = self.module._open_gff_and_fasta(filename)

        self.files_to_remove.append(self.path + filename + ".gff")
        self.files_to_remove.append(self.path + filename + "_data.gff")
        self.files_to_remove.append(self.path + filename + "_fasta.fasta")

        assert f_1.closed == False
        assert f_2.closed == False
        assert f_3.closed == False

        assert f_1.writable() == False
        assert f_2.writable() == True
        assert f_3.writable() == True

        self.streams_to_close.append(f_1)
        self.streams_to_close.append(f_2)
        self.streams_to_close.append(f_3)

    def test_separate_fasta_error(self):
        filename = "NoSuchFile"
        with pytest.raises(FileNotFoundError):
            assert self.module.separate_fasta(filename)

    def test_open_gff_and_fasta_error(self):
        filename = "NoSuchFile"
        with pytest.raises(FileNotFoundError):
            assert self.module._open_gff_and_fasta(filename)

    def teardown(self):
        for file in self.files_to_remove:
            os.remove(file)
        for stream in self.streams_to_close:
            stream.close()
