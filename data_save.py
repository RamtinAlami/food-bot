import csv

class csv_publisher:
    def __init__(self, filename, fieldnames):
        self.filename = filename
        self.fieldnames = fieldnames
    
    def init_file(self):
        with open(f"{self.filename}.csv", 'w+') as recipes_file:
            csv_writer = csv.DictWriter(recipes_file, fieldnames=self.fieldnames)
            csv_writer.writeheader()
        
    def write(self, input_dictionary):
        with open(f"{self.filename}.csv", 'a') as recipes_file:
            csv_writer = csv.DictWriter(recipes_file, fieldnames=self.fieldnames)
            csv_writer.writerow(input_dictionary)
