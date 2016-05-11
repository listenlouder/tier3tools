import csv
from os.path import expanduser


def get_list_from_csv(file_name):
    with open(file_name, 'rU') as f:
        reader = csv.reader(f)
        csv_list = list(reader)
    return csv_list


def build_control_dict(list1, list2):
    control_dict = {}
    for tn in list1:
        if tn[4] in list2:
            control_dict[tn[4]] = 50
        else:
            control_dict[tn[4]] = 5
    return control_dict


tn_list = get_list_from_csv('%s/Desktop/tn_report.csv' % expanduser('~'))
rate_centers = get_list_from_csv('%s/Desktop/rate_centers.csv' % expanduser('~'))[0]
rate_center_count = build_control_dict(tn_list, rate_centers)

output_list = []

for tn in tn_list:
    if rate_center_count[tn[4]] > 0:
        rate_center_count[tn[4]] -= 1
    elif rate_center_count[tn[4]] == 0:
        output_list.append(tn)


print 'WRITING TO FILE'
output_file = open('%s/Desktop/tn_fun_output.csv' % expanduser('~'), 'wb')
wr = csv.writer(output_file)
wr.writerows(output_list)
output_file.close()
print 'DONE'
