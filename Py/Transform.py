import pandas as pd
import json
from collections import defaultdict
import re
import time
from DB_Connect import create_connection

MAINDATA = 'Data/JobsData.csv'
DATAPATH = 'Data/'

jobdb = create_connection()
my_cursor = jobdb.cursor()
my_cursor.execute("USE job_desc_db;")

def demo_set_up():
    my_cursor.execute("delete from job_desc where job_desc_id >= 1")
    jobdb.commit()
    my_cursor.execute("delete from company where company_id >= 2")
    jobdb.commit()
    my_cursor.execute("delete from location where location_id >= 7")
    jobdb.commit()
    my_cursor.execute("delete from job where job_id >= 2")
    jobdb.commit()
#demo_set_up()

MAX_INT = 10000000000

df = pd.read_csv(MAINDATA)
def set_up_date(str):
    str = '2025-04-05'
    return str 
df['created_date'] = df['created_date'].apply(set_up_date)

def load_set_from(file_name):
    file_name += ".json"
    with open(file_name, "r", encoding="utf-8") as f:
        loaded = json.load(f)
    loaded_set = defaultdict(set, {k: set(v) for k, v in loaded.items()})
    return loaded_set

#SALARY TRANSFORMATION__________________________________________________________________________________________________________

currency = load_set_from(DATAPATH + "currency_archive")
unit = load_set_from(DATAPATH + "unit_archive")
hint_upper = {
    ">", ">=", "trên", "hơn", "từ",  
    "above", "over", "more", "minimum", "starting",
    "least", "from", "greater", "upwards" 
}
hint_lower = {
    "<", "<=", "dưới", "đến", "tới", "lên",  
    "under", "up", "to", "less", "maximum", "most",
    "below", "upto"
}

#transformation 
def find_currency(desc, str):
    if(str in set(currency["DEAL"])):
        return "DEAL"
    for word in reversed(desc):
        for key in currency:
            if word in currency[key]:
                return key
    return "VND"

def find_unit(str):
    for key in unit:
        if str in unit[key]:
            return int(key)
    return 1

def salary_transformation(salary_desc):
    salary_str = str(salary_desc).lower()
    salary_str.strip(' "')

    # Split the string 
    num = ""
    word = ""
    desc = []
    for ch in salary_str:
        if(ch.isdigit()):
            num += ch 
        elif ch == '.' or ch == ',' and num != "":
            num += '.'
        elif ch != '.' and ch != ';' and ch != ' ' and ch != '-':
            word += ch 
            if(num != ""): 
                desc.append(num)
                num = ""
        else:
            if(num != ""): desc.append(num)
            if(word != ""): desc.append(word)
            num = ""
            word = ""
    if(num != ""): desc.append(num)
    if(word != ""): desc.append(word)
  
    currency_found = find_currency(desc, salary_str)

    if currency_found == 'DEAL':
        return pd.Series([None, None, 'DEAL'], index=['min_salary', 'max_salary', 'currency'])
    if currency_found is None:
        return pd.Series([None, None, None], index=['min_salary', 'max_salary', 'currency'])

    mode = 1
    for index, item in enumerate(desc):
        try:
            temp1 = float(desc[index - 1])
            temp2 = float(desc[index ])
            mode = 2
            break 
        except:
            pass
    temp = 0.0
    unit_found = 1
    numbers = []
    for item in desc:
        if(currency_found == 'USD'):
            item = re.sub(r'[.]', '', item)
        try:
            temp = float(item)
            numbers.append(temp)
        except:
            temp = 0.0
            unit_found = 1
            unit_found *= find_unit(item)
            if(len(numbers) != 0): 
                numbers[-1] *= find_unit(item)
                if(mode == 2): numbers[0] *= unit_found
  
    for index, i in enumerate(numbers):
        numbers[index] = int(numbers[index])

    min_salary = None 
    max_salary = None 
    if(len(numbers) == 1):
        for item in desc:
            if item in hint_upper:
                min_salary = numbers[-1]
                break 
        if min_salary is None:
            for item in desc:
                if item in hint_lower:
                    max_salary = numbers[-1]
                    break 
        if min_salary is None and max_salary is None:
            min_salary = numbers[-1]
            max_salary = numbers[-1]
    elif(len(numbers) > 1):
        numbers.sort()
        min_salary = numbers[0]
        max_salary = numbers[-1]
    #return (min_salary, max_salary, currency)
    return pd.Series([min_salary, max_salary, currency_found], index = ['min_salary', 'max_salary', 'currency'])

#unit test for salary transformation
def salary_transformation_test():
    salary_test_case = {'salary': ["Trên 8 triệu", "1000 dollars to 1,500 dollars", "50 tr - 70 tr VND", "30m VND", "500 USD", "thuong luong", "up to 1,000,000 usd", "9-10trieu VND"]}
    df_salary_test = pd.DataFrame(salary_test_case)
    df_salary_test_out = pd.DataFrame()
    df_salary_test_out[['min_salary', 'max_salary', 'currency']] = df_salary_test['salary'].apply(salary_transformation)
    print(df_salary_test_out)
#THE END OF SALARY TRANSFORMATION_______________________________________________________________________________________________

#LOCATION TRANSFORMATION________________________________________________________________________________________________________ 

provinces = {
    "an giang", "bà rịa–vũng tàu", "bắc giang", "bắc kạn", "bạc liêu", "bắc ninh",
    "bến tre", "bình định", "bình dương", "bình phước", "bình thuận",
    "cà mau", "cần thơ", "cao bằng", "đà nẵng", "đắk lắk", "đắk nông",
    "điện biên", "đồng nai", "đồng tháp", "gia lai", "hà giang", "hà nam",
    "hà nội", "hà tĩnh", "hải dương", "hải phòng", "hậu giang", "hòa bình",
    "hưng yên", "khánh hòa", "kiên giang", "kon tum", "lai châu", "lâm đồng",
    "lạng sơn", "lào cai", "long an", "nam định", "nghệ an", "ninh bình",
    "ninh thuận", "phú thọ", "phú yên", "quảng bình", "quảng nam",
    "quảng ngãi", "quảng ninh", "quảng trị", "sóc trăng", "sơn la",
    "tây ninh", "thái bình", "thái nguyên", "thanh hóa", "thừa thiên huế",
    "tiền giang", "hồ chí minh", "trà vinh", "tuyên quang", "vĩnh long",
    "vĩnh phúc", "yên bái", "nước ngoài"
}

cities = {
    "hà nội", "hồ chí minh", "đà nẵng", "hải phòng", "cần thơ", "huế",
    "an khê", "bà rịa", "bạc liêu", "bắc giang", "bắc kạn", "bắc ninh", "bảo lộc",
    "bến tre", "biên hòa", "biên hoà", "buôn ma thuột", "cà mau", "cẩm phả", "cam ranh",
    "cao bằng", "cao lãnh", "châu đốc", "chí linh", "đà lạt", "điện biên phủ",
    "đông hà", "đồng hới", "đồng xoài", "gia nghĩa", "hà giang", "hà tiên",
    "hạ long", "hòa bình", "hội an", "huế", "kon tum", "lào cai", "long xuyên",
    "móng cái", "mỹ tho", "nam định", "nha trang", "ninh bình", "phan rang-tháp chàm",
    "phan thiết", "phủ lý", "pleiku", "quảng ngãi", "quy nhơn", "rạch giá",
    "sa đéc", "sóc trăng", "sơn la", "tam kỳ", "tân an", "thái bình",
    "thái nguyên", "thanh hóa", "thủ dầu một", "trà vinh", "tuy hòa", "tuyên quang",
    "uông bí", "việt trì", "vinh", "vĩnh long", "vĩnh yên", "vũng tàu", "yên bái"
}

removable = [
    "tp", "thanh pho", "thành phố", "quận"
]


def location_transformation(str):
    str = str.lower()
    desc = re.split(r"[:,;]", str)
    for index, item in enumerate(desc):
        desc[index] = desc[index].strip(' "')

    #extract locations
    location_found = []
    province_found = None
    city_found = None
    district_found = None
    prev = ''
    inserted = False
    for item in desc:
        for tp in removable:
            if item.startswith(tp):
                item = item[len(tp):].lstrip()
                break
        if item in provinces:
            if item == "nước ngoài":
                location_found.append((item, None, None))
                continue
            if city_found is not None and district_found is None:
                location_found.append((province_found, city_found, district_found))
                inserted = True
            province_found = item
            prev = 'p'
            inserted = False
            city_found = None 
            district_found = None
            if item in cities:
                city_found = item
                prev = 'pc' 
            continue
        if item in cities:
            district_found = None
            if prev == 'c' or prev == 'pc':
                location_found.append((province_found, city_found, district_found))
                city_found = item
                inserted = True
                continue 
            city_found = item
            prev = 'c'
            inserted = False
            continue
        location_found.append((province_found, city_found, item))
        district_found = item
        prev = 'd'
        inserted = True
    if(inserted == False):
        location_found.append((province_found, city_found, district_found))

    return(location_found)

def location_transformation_test():
    location_test_case = ["Đồng Nai: Biên Hoà", "Bến Tre: TP Bến Tre", "Hà Nội: Cầu Giấy", "Hồ Chí Minh", "Hồ Chí Minh: Tân Bình: Hà Nội: Ba Đình", "Nghệ An, Vinh : Hà Nội, Cầu Giấy, Hà Đông, Ba Đình, Hồ Chí Minh : Tân Bình, Hồ Chí minh, Quận 1"]
    for test in location_test_case:
        print(location_transformation(test))

#THE END OF LOCATION TRANSFORMATION______________________________________________________________________________________________ 

#JOB TRANSFORMATION______________________________________________________________________________________________________________ 
non_classified_job = 0
non_classified_experience = 0

fields = load_set_from(DATAPATH + "fields_archive")
experiences = load_set_from(DATAPATH + "experiences_archive")

def is_field(item):
    for field in fields:
        if item in fields[field]:
            return field 
    return None

def is_experience(item):
    for experience in experiences:
        if item in experiences[experience]:
            return experience
    return None

def find_field(index, desc, n):
    field_found = is_field(desc[index])
    if index < n - 1:
        temp = is_field(desc[index] + ' ' + desc[index + 1])
        field_found = temp if temp is not None else field_found
        if field_found is None:
            temp = is_field(desc[index] + desc[index + 1])
            field_found = temp if temp is not None else field_found
    if index < n - 2:
        temp = is_field(desc[index] + ' ' + desc[index + 1] + ' ' + desc[index + 2])
        field_found = temp if temp is not None else field_found
        if field_found is None:
            temp = is_field(desc[index] + ' ' + desc[index + 2])
            field_found = temp if temp is not None else field_found
    if index < n - 3:
        temp = is_field(desc[index] + ' ' + desc[index + 1] + ' ' + desc[index + 2] + ' ' + desc[index + 3])
        field_found = temp if temp is not None else field_found
    return field_found

def find_experience(index, desc, n):
    experience_found = is_experience(desc[index])
    if index < n - 1:
        temp = is_experience(desc[index] + ' ' + desc[index + 1])
        experience_found = temp if temp is not None else experience_found
        if experience_found is None:
            temp = is_experience(desc[index] + desc[index + 1])
            experience_found = temp if temp is not None else experience_found
    return experience_found

def job_transformation(str):
    global non_classified_job
    str = str.lower()
    desc = re.split(r"[ _\-,:/()]", str)
    n = len(desc)
    for index, item in enumerate(desc):
        field_found = find_field(index, desc, n)
        if field_found is not None:
            return pd.Series([str, field_found], index = ['job_desc', 'field'])
    non_classified_job += 1
    return pd.Series([str, None], index = ['job_desc', 'field'])

def experience_transformation(str):
    global non_classified_experience
    str = str.lower()
    desc = re.split(r"[ _\-,:/()]", str)
    n = len(desc)
    for index, item in enumerate(desc):
        experience_found = find_experience(index, desc, n)
        if experience_found is not None:
            return experience_found
    non_classified_experience += 1
    return None

#THE END OF JOB TRANSFORMATION___________________________________________________________________________________________________ 

#COMPANY TRANSFORMATION__________________________________________________________________________________________________________ 
def company_transformation(str):
    str = str.upper()
    desc = re.split(r"[ _\-,:/()]", str)
    str = ""
    for item in desc:
        if item != '':
            str += item + ' '
    return str.strip(" ")
#THE END OF COMPANY TRANSFORMATION_______________________________________________________________________________________________ 

#TIME TRANSFORMATION_____________________________________________________________________________________________________________

def time_transformation(created_at, expired_str):
    expired_at = ""
    for index, ch in enumerate(expired_str):
        if ch >= '0' and ch <= '9':
            for i in range(index, len(expired_str)):
                if not (expired_str[i] >= '0' and expired_str[i] <= '9'):
                    break
                expired_at += expired_str[i]
            break
    return(created_at, int(expired_at))

#THE END OF TIME TRANSFORMATION__________________________________________________________________________________________________

#MAIN TRANSFORMATION_____________________________________________________________________________________________________________

def reset_auto_increment(table_name):
    my_cursor.execute(f"SELECT MAX({table_name + '_id'}) FROM {table_name}")
    max_id = my_cursor.fetchone()[0] or 0
    next_id = max_id + 1
    my_cursor.execute(f"ALTER TABLE {table_name} AUTO_INCREMENT = {next_id}")
    jobdb.commit()

class TRANSFORM():
    def transform_salary():
        df_salary_out = pd.DataFrame()
        df_salary_out[['min_salary', 'max_salary', 'currency']] = df['salary'].apply(salary_transformation)
        df_salary_out.to_csv(DATAPATH + 'TransformedSalary.csv', index = False)

    def transform_job_desc():
        global non_classified_job
        global non_classified_experience
        # reset_auto_increment("job")

        df_jobdesc_out = pd.DataFrame()
        df_jobdesc_out = df['job_title'].apply(job_transformation)
        df_jobdesc_out['experience'] = df["job_title"].apply(experience_transformation)
        list_jobid = []

        for row in df_jobdesc_out.itertuples(index = True):
            if row.field is not None and row.experience is not None: 
                my_cursor.execute("select job_id from job where field = %s and experience = %s", (row.field, row.experience))
            elif row.field is None and row.experience is not None:
                my_cursor.execute("select job_id from job where field is Null and experience = %s", (row.experience,))
            elif row.field is not None and row.experience is None:
                my_cursor.execute("select job_id from job where field = %s and experience is Null", (row.field,))
            else:
                my_cursor.execute("select job_id from job where field is Null and experience is Null")
            try:
                job_idx = my_cursor.fetchone()[0]
            except:
                my_cursor.execute(f"insert into job(field, experience) values (%s, %s)", (row.field, row.experience))
                jobdb.commit()
                my_cursor.execute("select max(job_id) from job")
                job_idx = my_cursor.fetchone()[0]
            list_jobid.append(job_idx)
        df_jobdesc_out.insert(3, 'job_id', list_jobid)
        df_jobdesc_out.to_csv(DATAPATH + 'Transformed_JobDesc.csv', index = False)
        print(f"There are {non_classified_job} unclassified jobs.")
        print(f"There are {non_classified_experience} unclassified experience requirements.")

    def transform_time():
        pd.DataFrame((time_transformation(row.created_date, row.time) for row in df.itertuples(index = False)), columns = ['created_at', 'expired_at']).to_csv(DATAPATH + 'TransformedTime.csv', index = False)

    def transform_company_location():
        global my_cursor
        global df

        reset_auto_increment("location")
        reset_auto_increment("company")

        my_cursor.execute("select company_id, company_name, location.location_id from company join location where location.location_id = company.location_id")
        company_location = my_cursor.fetchall()
        companies_lookup = {
            (item[1], item[2]) : item[0]
            for item in company_location
        }
        my_cursor.execute("select * from location")
        company_location = my_cursor.fetchall()
        locations_lookup = {
            (item[1], item[2], item[3]) : item[0]
            for item in company_location
        }

        df_company_location_out = pd.DataFrame(columns = ['index', 'company_id', 'location_id'])
        len_cl_out = 0

        for row in df.itertuples(index = True):
            company_found = company_transformation(row.company)
            for location_found in location_transformation(row.address):
                if location_found == (None, None, None): 
                    continue
                loc_idx = locations_lookup.get(location_found)
                if loc_idx is not None:
                    comp_idx = companies_lookup.get((company_found, loc_idx))
                    if comp_idx is not None:
                        df_company_location_out.loc[len_cl_out] = [row.Index, comp_idx, loc_idx]
                        len_cl_out += 1
                    else:
                        my_cursor.execute("insert into company(company_name, location_id) values (%s, %s);", (company_found, loc_idx))
                        jobdb.commit()
                        my_cursor.execute("select max(company_id) from company;")
                        comp_idx = my_cursor.fetchone()[0]
                        companies_lookup[(company_found, loc_idx)] = comp_idx
                        df_company_location_out.loc[len_cl_out] = [row.Index, comp_idx, loc_idx]
                        len_cl_out += 1
                else:
                    my_cursor.execute("insert into location(province, city, district) values (%s, %s, %s);", location_found)
                    jobdb.commit()
                    my_cursor.execute("select max(location_id) from location;")
                    loc_idx = my_cursor.fetchone()[0]
                    locations_lookup[location_found] = loc_idx

                    comp_idx = companies_lookup.get((company_found, loc_idx))
                    if comp_idx is not None:
                        df_company_location_out.loc[len_cl_out] = [row.Index, comp_idx, loc_idx]
                        len_cl_out += 1
                    else:
                        my_cursor.execute("insert into company(company_name, location_id) values (%s, %s);", (company_found, loc_idx))
                        jobdb.commit()
                        my_cursor.execute("select max(company_id) from company;")
                        comp_idx = my_cursor.fetchone()[0]
                        companies_lookup[(company_found, loc_idx)] = comp_idx
                        df_company_location_out.loc[len_cl_out] = [row.Index, comp_idx, loc_idx]
                        len_cl_out += 1
        df_company_location_out.to_csv(DATAPATH + 'Transformed_CompanyLocation.csv', index = False)
        # testdf = pd.DataFrame({
        # 'address': ["hà nội : nam từ liêm, Thừa Thiên Huế: TP Huế", "hà nội : hoàn kiếm", "hà nội: cầu giấy"],
        # 'company': ['công ty cổ phần rikkeisoft', 'Công ty Cổ phần Công nghệ KiotViet', 'Công ty Cổ phần VNEXT SOFTWARE']
        # }) --test cases for this function

#THE END OF MAIN TRANSFORMATION__________________________________________________________________________________________________

start_time = time.time()
TRANSFORM.transform_salary()
TRANSFORM.transform_job_desc()
TRANSFORM.transform_time()
TRANSFORM.transform_company_location()
print(f"Execution time: {time.time() - start_time}")

#UNIT TEST_______________________________________________________________________________________________________________________
# df['company'].apply(company_transformation)
# salary_transformation_test()
# location_transformation_test()
# for row in df.itertuples():
#     print(time_transformation(row.created_date, row.time))
#THE END OF UNIT TEST____________________________________________________________________________________________________________

jobdb.close()