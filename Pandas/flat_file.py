import pandas as pd

def main():
    df_person = pd.read_csv('basic_person.csv')
    df_student = pd.read_csv('person_detail_f.csv')
    df_map = pd.read_csv('student_detail_v.csv')
    df_max = df_map.groupby('student_id_new').agg({
        'acct_id_new': 'max',
        'person_detail_id_new': 'max'
    }).reset_index()
    
    df_joined = pd.merge(df_max, df_student, on='person_detail_id_new', how='left')
    df_final = pd.merge(df_joined, df_person, on='acct_id_new', how='left')
    df_final.to_csv('joined.csv', index=False)

if __name__ == '__main__':
    main()