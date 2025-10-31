# flat_file.py
import pandas as pd


def main():
    # Load and process the files.
    # Save the file 'joined.csv' without the implicit index
    df_person = pd.read_csv('basic_person.csv')
    df_student = pd.read_csv('person_detail_f.csv')
    df_map = pd.read_csv('student_detail_v.csv')
    df_joined = df_map.groupby("student_id_new").max().reset_index()
    df_joined = df_joined.join(df_person.set_index('acct_id_new'), on='acct_id_new')
    df_joined = df_joined.join(df_student.set_index('person_detail_id_new'), on='person_detail_id_new')
    df_joined.to_csv('joined.csv', index=False)  


if __name__ == '__main__':
    main()