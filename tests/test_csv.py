import pytest
import os

from mparser import csv

class TestCSVPreparationManager:
    def setup(self):
        self.path = 'testgff/'
        self.module = csv.CSVPreparationManager(path=self.path, output=self.path)

        self.files_to_remove = []
        self.streams_to_close = []

    def test_gff_csv_stream(self):
        filename = "SampleGff"

        f1, f2 = self.module._gff_csv_stream(filename)

        self.files_to_remove.append(self.path + "SampleGff.csv")
        self.streams_to_close.append(f1)
        self.streams_to_close.append(f2)

        assert f1.closed == False
        assert f2.closed == False

        assert f1.writable() == False
        assert f2.writable() == True

    def test_gff_csv_stream_error(self):
        filename = "NoSuchFile"

        with pytest.raises(FileNotFoundError):
            assert self.module._gff_csv_stream(filename)

    def test_parse_gene_details(self):
        details_1 = "ID=10_a;Name=testname;"
        assert self.module._parse_gene_details(details_1) == ("10_a", "testname")

        details_2 = "ID=:10_a;Name=testname;"
        assert self.module._parse_gene_details(details_2) == ("10_a", "testname")

        details_3 = "Name=testname;param=value;ID=:10_b;"
        assert self.module._parse_gene_details(details_3) == ("10_b", "testname")

    def test_parse_gene_details_error(self):
        details_1 = "ID=10ui,Name=testName;"
        with pytest.raises(Exception):
            assert self.module._parse_gene_details(details_1)

        details_2 = "ID=10ui"
        with pytest.raises(Exception):
            assert self.module._parse_gene_details(details_2)

    def test_parse_line_to_csv_line(self):
        gff_line = "2L	Drosophila_2	oligonucleotide	122928	122952	.	-	.	ID=1641004_a_at_2443_oligonucleotide;Name=1641004_a_at_2443;Dbxref=Affymetrix:1641004_a_at_2443;"
        expected_line = "1641004_a_at_2443,1641004_a_at_2443_oligonucleotide,2L,oligonucleotide,-,122928,122952"

        assert self.module._parse_line_to_csv_line(gff_line) == expected_line

    def test_parse_line_to_csv_line_error(self):
        gff_line_1 = "2L  droso"

        with pytest.raises(Exception):
            self.module._parse_line_to_csv_line(gff_line_1)

        gff_line_2 = "2L	Drosophila_2	oligonucleotide	122928	122952	.	?	.	ID=1641004_a_at_2443_oligonucleotide;Name=1641004_a_at_2443;Dbxref=Affymetrix:1641004_a_at_2443;"
        with pytest.raises(Exception):
            self.module._parse_line_to_csv_line(gff_line_2)

        gff_line_3 = "2L	Drosophila_2	oligonucleotide	a	b	.	-	.	ID=1641004_a_at_2443_oligonucleotide;Name=1641004_a_at_2443;Dbxref=Affymetrix:1641004_a_at_2443;"
        with pytest.raises(Exception):
            self.module._parse_line_to_csv_line(gff_line_3)

        gff_line_4 = "2L	Drosophila_2	oligonucleotide	101	b	.	-	.	ID=1641004_a_at_2443_oligonucleotide;Name=1641004_a_at_2443;Dbxref=Affymetrix:1641004_a_at_2443;"
        with pytest.raises(Exception):
            self.module._parse_line_to_csv_line(gff_line_4)

        gff_line_5 = "2L	Drosophila_2	oligonucleotide	a	100	.	-	.	ID=1641004_a_at_2443_oligonucleotide;Name=1641004_a_at_2443;Dbxref=Affymetrix:1641004_a_at_2443;"
        with pytest.raises(Exception):
            self.module._parse_line_to_csv_line(gff_line_5)

    def test_gff_data_to_csv(self):
        filename = "SampleGff"
        self.module.gff_data_to_csv(filename)

        self.files_to_remove.append(self.path + filename + ".csv")

        headline = "name,ID,chr,feature,strand,start,end"
        expected_line_1 = "9754052,9754052_na_dbEST.diff.dmel,2L,match_part,+,108588,108809"
        expected_line_2 = "hmm3410,NCBI_gnomon:CG_NCBI_GNO_32003410_caf1,2L,match,+,108686,113539"
        expected_line_3 = "ncbi_aa_935147,ncbi_aa_935147_aa_ncbi_other,2L,match_part,-,119832,119990"
        expected_line_4 = "1641004_a_at_2470,1641004_a_at_2470_oligonucleotide,2L,oligonucleotide,-,122901,122925"

        with open(self.path + filename + ".csv") as f:
            content = f.read()

        lines = content.split("\n")

        assert lines[0] == headline
        assert lines[1] == expected_line_1
        assert lines[2] == expected_line_2
        assert lines[3] == expected_line_3
        assert lines[4] == expected_line_4

    def teardown(self):
        for file in self.files_to_remove:
            os.remove(file)
        for stream in self.streams_to_close:
            stream.close()

