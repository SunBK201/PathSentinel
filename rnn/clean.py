import shutil
shutil.copy2("rnn/dataset/attack.txt", "rnn/dataset/attack_backup.txt")
shutil.copy2("rnn/dataset/normal.txt", "rnn/dataset/normal_backup.txt")

with open("rnn/dataset/attack.txt", "r+") as file:
    lines = set(file.readlines())
    lines = sorted(list(lines))

    file.seek(0)
    file.truncate()

    file.writelines(lines)

with open("rnn/dataset/normal.txt", "r+") as file:
    lines = set(file.readlines())
    lines = sorted(list(lines))

    file.seek(0)
    file.truncate()

    file.writelines(lines)