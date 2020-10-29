import csv


def class_rosters(input_file, year=2020):
    """Read the input_file and modify the data
    according to the Bite description.
    Return a list holding one item per student
    per class, correctly formatted."""

    with open(input_file) as fp:
        headers = "id name".split()
        csvfile = csv.DictReader(fp.readlines(), headers, restkey="Classes")

    assignments = []

    for student in csvfile:
        idx = student.get("id")
        classes = student.get("Classes")

        for c in classes:
            if c:
                c_name, _ = c.split(" - ")
                assignments.append(f"{c_name},{year},{idx}")

    return assignments


if __name__ == "__main__":
    print(class_rosters("full.csv"))
