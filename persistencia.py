from abc import ABC, abstractmethod 

#interfaz
class IPersistence(ABC):
    @abstractmethod
    def save(self,data: list[dict]):
        pass
    @abstractmethod
    def load(self):
        pass

class PersistenceCsv(IPersistence):
    def __init__(self, file_name):
        self.file_name = file_name

    def save(self, data):
        if not data:
            f = open(self.file_name, "w")
            f.close()
            return
        
        
        key = data[0].keys()
        csv_content = ",".join(key) + "\n"
        for d in data:
            values_as_string = []
            for value in d.values():
                values_as_string.append(str(value))
            file_csv = ",".join(values_as_string) + "\n"
            csv_content = csv_content + file_csv
        
        f = None
        try:
            f = open(self.file_name, "w")
            f.write(csv_content)
        except Exception as e:
            print(f"Error al guardar en: {self.file_name}: {e}")
        
        finally:
            if f:
                f.close()

    def load(self):
        f = None
        try:
            f = open(self.file_name, 'r')
            content = f.read()
        except FileNotFoundError:
            return []
        finally:
            if f:
                f.close()

        if content == "":
            return []
        
        rows = content.split("\n")

        if rows[-1] == "":
            rows.pop()

        first_row = rows[0]
        headers = first_row.split(",")
        data_raws_strings = rows[1:]

        loaded_data = []
        for row_string in data_raws_strings:
            values_list = row_string.split(",")
            appointment_dict = dict(zip(headers,values_list))
            
            loaded_data.append(appointment_dict)
        
        return loaded_data