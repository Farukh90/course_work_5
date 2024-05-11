import psycopg2

red_col = '\033[91m'
reset_red_col = '\033[0m'


def connector(database: str = 'course_work_5_fj', password: str = '123', host: str = 'localhost', user: str = 'postgres'):
    '''коннектор для соединения с БД. при вызове можно передать другие аргументы '''
    conn = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password
    )
    return conn


def tables_creator(con, con_status: int = 0, table_name_1: str = 'employers', table_name_2: str = 'vacancies'):
    '''создает таблицы. названия по умолчанию прописаны согласно ДЗ'''
    try:
        with con:
            with con.cursor() as cur:
                cur.execute(f'''CREATE TABLE {table_name_1}
                            (
                                employer_id INT PRIMARY KEY,
                                employer VARCHAR(100) NOT NULL
                            )''')

                cur.execute(f'''CREATE TABLE {table_name_2}
                            (  
                                vacancy_id SERIAL PRIMARY KEY,
                                employer_id INT NOT NULL,
                                region VARCHAR(100) NOT NULL,
                                vacancy VARCHAR(100) NOT NULL,
                                salary INT NOT NULL,
                                currency VARCHAR(100),
                                requirement TEXT,
                                vacancy_url VARCHAR(100)NOT NULL,
                                FOREIGN KEY (employer_id) REFERENCES employers(employer_id)
                            )''')

    except psycopg2.Error as e:
        print('произошла', e)

    finally:
        if con_status == 0:
            if con is not None:
                con.close()


def loads_into_table(con, vacansies: list):
    '''заполняет таблицу данными о вакансиях'''
    try:
        with con:
            with con.cursor() as cur:
                for vac in vacansies:
                    cur.execute('INSERT INTO employers (employer_id, employer) VALUES '
                                '(%s,%s)' 'ON CONFLICT (employer_id) DO NOTHING', (vac.employer_id, vac.employer_name))

                    cur.execute(f'INSERT INTO vacancies '
                                f'(employer_id, region, vacancy, salary, currency, requirement, vacancy_url) '
                                f'VALUES ''(%s,%s,%s,%s,%s,%s,%s)',
                                (vac.employer_id, vac.region, vac.vacancy_name, vac.salary, vac.currency, vac.requirement, vac.vacancy_url))

    except psycopg2.Error as e:
        print('произошла', e)

    finally:
        if con is not None:
            con.close()


def drop_table(con, table_name, con_status: int = 0):
    '''удаляет таблицу. по умолчанию соединение закроется. если передать в con_status 1 то останется открытым'''
    try:
        with con:
            with con.cursor() as cur:
                cur.execute(f"DROP TABLE {table_name}")
                print(f'{red_col}из базы данных удалена таблица {table_name}{reset_red_col}')

    except psycopg2.Error as e:
        print('произошла', e)

    finally:
        if con_status == 0:
            if con is not None:
                con.close()
