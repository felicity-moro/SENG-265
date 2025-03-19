 for element in self.__patients.values():
            print(element.name)
            if to_find in element.name:
                retrieved.append(element)