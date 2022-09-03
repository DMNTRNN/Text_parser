
import csv

# Данная функция преобразует словарь, по которому производится поиск, в сет
def set_creator(filename):
    db = open(filename, encoding='utf-8', newline='')
    db_reader = csv.reader(db)
    db_set = set()
    for name in db_reader:
        db_set.add(name[0].lower())
    db.close()
    return db_set

    
# Данная функция проверяет наличие пересекающихся элементов в двух сетах. При существовании положительного срабатывания
# в текущем диалоге возвращает пустую строку, таким образом для каждого диалога возможно только однократное появление единицы 
# в соответствующем статусе
def check_line(overall_set, unique_words, status):
    if status > 1:
        return ''
    overlap = overall_set.intersection(unique_words)
    if overlap !=set():
        return 1
    else:
        return ''
    
    
# Данная функция позволяет доставать из текста названия компании и имя менеджера, они точно также, имя и название в статусе диалога
# появляется только один раз - когда умпоминается впервые    
def get_name(overall_set, unique_words, status):
    if status > 1:
        return ''
    overlap = overall_set.intersection(unique_words)
    if overlap !=set():
        return list(overlap)[0]
    else:
        return ''    
    
    
# Функция для составления сета, так как в ключевых словах и выражениях содержатся выражения длиной до двух слов
# данная функция рабивает строку на списки из одного и двух слов      
def set_constructor(list_of_words):
    for  i in range(len(list_of_words)-1):
        list_of_words.append(list_of_words[i] + ' ' + list_of_words[i+1])
    return list_of_words  


# Функция для обработки диалога. Данная функция также записывает результаты в новый csv файл - добавляются 
# пять новых столбцов, куда записываются результаты парсинга     
def dialogue_processing(name_for_processed_database, dialogue, names, companies, greetings, farewells):
    greeting_status_counter = 0
    farewell_status_counter = 0
    name_counter = 0
    company_counter = 0
    overall_status_counter = 0
    overall_status = ''
    for line in dialogue:
        if line[2] == 'manager':          
            greeting_status = check_line(greetings, line[-1], greeting_status_counter)
            if greeting_status == 1:
                greeting_status_counter+=1
            farewell_status = check_line(farewells, line[-1], farewell_status_counter)
            if farewell_status == 1:
                farewell_status_counter+=1
            name = get_name(names, line[-1], name_counter)
            if name != '':
                name_counter+=1
            company = get_name(companies, line[-1], company_counter)
            if company != '':
                company_counter+=1
            if farewell_status_counter > 0 and greeting_status_counter > 0:
                overall_status_counter+=1
            if farewell_status_counter > 0 and greeting_status_counter > 0 and overall_status_counter == 1:
                overall_status = 1
            else:
                overall_status = ''
            print(line[0])
            new_file = open(name_for_processed_database +'.csv', 'a', encoding='utf-8')
            writer = csv.writer(new_file)
            writer.writerow([line[0], line[1], line[2], line[3], str(greeting_status), str(farewell_status), name, company, str(overall_status)])
            new_file.close()
        else:
            new_file = open(name_for_processed_database +'.csv', 'a', encoding='utf-8')
            writer = csv.writer(new_file)
            writer.writerow([line[0], line[1], line[2], line[3], '', '', '', '', ''])
            new_file.close()
 

#Данная функция отвечает за обработку файла. Она считывает файл с помощью генератора, чтобы была возможность обработки
#файлов большого объема           
def data_processing( processing_function, dictionaries, initial_database, name_for_processed_database):
    names = dictionaries[0]
    companies = dictionaries[1]
    greetings = dictionaries[2]
    farewells = dictionaries[3]
    data_base = open(initial_database, encoding='utf-8-sig')
    text_data = csv.reader(data_base)
    first_line = next(text_data)
    # data_base.close()
    new_file = open(name_for_processed_database+'.csv', 'a', encoding='utf-8')
    writer = csv.writer(new_file)
    writer.writerow(first_line + ['greeting_status', 'farewell_status', 'name', 'company', 'overall_status'])
    new_file.close()
    dialogue_number = None
    for line in text_data:
        if dialogue_number == None:
            dialogue_number = 0
            dialogue =[] # инициализируем список для функции обработки диалогов
        if dialogue_number != int(line[0]):
            dialogue_processing(name_for_processed_database, dialogue, names, companies, greetings, farewells)
            dialogue = []
        text_string = line[3].lower()
        dialogue_number = int(line[0])
        doc = text_string.split(' ')
        doc = set_constructor(doc)
        unique_words = set(doc)
        dialogue.append((line[0], line[1], line[2], line[3], unique_words))
    dialogue_processing(name_for_processed_database, dialogue, names, companies, greetings, farewells)
    

names = set_creator('rus_names.csv')# словарь имен менеджеров
companies = set_creator('companies.csv')# словарь названий компаний
greetings = set_creator('greetings.csv')# словарь приветствий
farewells = set_creator('farewells.csv')# словарь прощаний


data_processing(dialogue_processing, [names, companies, greetings, farewells],  'test_data.csv', 'processed_data')            
    
    
    
    
    
    
    
    
    
    
