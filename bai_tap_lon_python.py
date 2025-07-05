import json
import os

subjects = {}

# =================== Utility functions ===================
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def save_to_file(filename="study_plan.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(subjects, f, ensure_ascii=False, indent=4)

def load_from_file(filename="study_plan.json"):
    global subjects
    try:
        with open(filename, "r", encoding="utf-8") as f:
            subjects = json.load(f)
    except FileNotFoundError:
        pass

# =================== Core Functions ===================
def add_subject():
    name = input("Nhập tên môn học: ").strip()
    if name in subjects:
        return "Môn học đã tồn tại."
    subjects[name] = {"documents": [], "goals": [], "notes": ""}
    return "Đã thêm môn học."

def view_subjects():
    if not subjects:
        return "Chưa có môn học nào."
    return "\n".join(f"{i+1}. {name}" for i, name in enumerate(subjects))

def edit_subject():
    name = input("Nhập tên môn học cần sửa: ").strip()
    if name not in subjects:
        return "Môn học không tồn tại."
    new_name = input("Nhập tên mới: ").strip()
    if not new_name:
        return "Tên mới không hợp lệ."
    subjects[new_name] = subjects.pop(name)
    return "Đã sửa tên môn học."

def delete_subject():
    name = input("Nhập tên môn học cần xóa: ").strip()
    if name not in subjects:
        return "Môn học không tồn tại."
    del subjects[name]
    return "Đã xóa môn học."

def add_document():
    name = input("Nhập tên môn học: ").strip()
    if name not in subjects:
        return "Môn học không tồn tại."
    doc = input("Nhập tên tài liệu: ").strip()
    subjects[name]['documents'].append(doc)
    return "Đã thêm tài liệu."

def view_documents():
    name = input("Nhập tên môn học: ").strip()
    if name not in subjects:
        return "Môn học không tồn tại."
    docs = subjects[name]['documents']
    return "\n".join(f"- {doc}" for doc in docs) if docs else "Chưa có tài liệu."

def delete_document():
    name = input("Nhập tên môn học: ").strip()
    if name not in subjects:
        return "Môn học không tồn tại."
    doc = input("Nhập tên tài liệu muốn xóa: ").strip()
    try:
        subjects[name]['documents'].remove(doc)
        return "Đã xóa tài liệu."
    except ValueError:
        return "Không tìm thấy tài liệu."

def add_goal():
    name = input("Nhập tên môn học: ").strip()
    if name not in subjects:
        return "Môn học không tồn tại."
    goal = input("Nhập mục tiêu: ").strip()
    deadline = input("Hạn hoàn thành (YYYY-MM-DD): ").strip()
    subjects[name]['goals'].append({'goal': goal, 'deadline': deadline, 'done': False})
    return "Đã thêm mục tiêu."

def view_goals():
    name = input("Nhập tên môn học: ").strip()
    if name not in subjects:
        return "Môn học không tồn tại."
    goals = subjects[name]['goals']
    if not goals:
        return "Chưa có mục tiêu."
    return "\n".join(f"{i+1}. {g['goal']} - {g['deadline']} [{'✓' if g['done'] else '✗'}]" for i, g in enumerate(goals))

def mark_goal_done():
    name = input("Nhập tên môn học: ").strip()
    if name not in subjects or not subjects[name]['goals']:
        return "Môn học không tồn tại hoặc chưa có mục tiêu."
    print(view_goals_for(name))
    idx = int(input("Nhập số mục tiêu đã hoàn thành: ")) - 1
    if 0 <= idx < len(subjects[name]['goals']):
        subjects[name]['goals'][idx]['done'] = True
        return "Đã đánh dấu hoàn thành."
    return "Số thứ tự không hợp lệ."

def view_goals_for(name):
    return "\n".join(f"{i+1}. {g['goal']} - {g['deadline']} [{'✓' if g['done'] else '✗'}]" for i, g in enumerate(subjects[name]['goals']))

def delete_goal():
    name = input("Nhập tên môn học: ").strip()
    if name not in subjects or not subjects[name]['goals']:
        return "Môn học không tồn tại hoặc chưa có mục tiêu."
    print(view_goals_for(name))
    idx = int(input("Nhập số thứ tự mục tiêu muốn xóa: ")) - 1
    if 0 <= idx < len(subjects[name]['goals']):
        subjects[name]['goals'].pop(idx)
        return "Đã xóa mục tiêu."
    return "Số thứ tự không hợp lệ."

def progress_report():
    total = sum(len(data['goals']) for data in subjects.values())
    done = sum(g['done'] for data in subjects.values() for g in data['goals'])
    return f"Đã hoàn thành {done}/{total} mục tiêu." if total else "Chưa có mục tiêu nào."

def add_note():
    name = input("Nhập tên môn học: ").strip()
    if name not in subjects:
        return "Môn học không tồn tại."
    note = input("Nhập ghi chú: ").strip()
    subjects[name]['notes'] = note
    return "Đã thêm ghi chú."

def view_note():
    name = input("Nhập tên môn học: ").strip()
    return subjects[name]['notes'] if name in subjects else "Môn học không tồn tại."

def delete_note():
    name = input("Nhập tên môn học: ").strip()
    if name in subjects:
        subjects[name]['notes'] = ""
        return "Đã xóa ghi chú."
    return "Môn học không tồn tại."

def search_subject():
    keyword = input("Nhập từ khóa: ").lower()
    result = [s for s in subjects if keyword in s.lower()]
    return "\n".join(result) if result else "Không tìm thấy môn học."

def search_document():
    keyword = input("Nhập từ khóa tài liệu: ").lower()
    found = []
    for sub, data in subjects.items():
        for doc in data['documents']:
            if keyword in doc.lower():
                found.append(f"- {doc} ({sub})")
    return "\n".join(found) if found else "Không tìm thấy tài liệu."

def export_report():
    filename = input("Tên file xuất (.txt): ").strip()
    with open(filename, "w", encoding="utf-8") as f:
        for name, data in subjects.items():
            f.write(f"Môn: {name}\n")
            f.write("  Tài liệu:\n")
            for doc in data['documents']:
                f.write(f"    - {doc}\n")
            f.write("  Mục tiêu:\n")
            for g in data['goals']:
                status = "✓" if g['done'] else "✗"
                f.write(f"    - {g['goal']} - {g['deadline']} [{status}]\n")
            f.write(f"  Ghi chú: {data['notes']}\n\n")
    return "Đã xuất báo cáo."

menu = {
    "1": add_subject, "2": view_subjects, "3": edit_subject, "4": delete_subject,
    "5": add_document, "6": view_documents, "7": delete_document,
    "8": add_goal, "9": view_goals, "10": mark_goal_done, "11": delete_goal,
    "12": progress_report, "13": add_note, "14": view_note, "15": delete_note,
    "16": search_subject, "17": search_document, "18": export_report,
    "19": save_to_file, "20": load_from_file
}

load_from_file()

menu_text = """
===== MENU =====
1. Thêm môn học mới
2. Xem danh sách các môn học
3. Sửa tên môn học
4. Xóa môn học
5. Thêm tài liệu cần đọc cho môn học
6. Xem tài liệu của môn học
7. Xóa tài liệu khỏi môn học
8. Thêm mục tiêu học tập cho môn học
9. Xem danh sách mục tiêu học tập
10. Đánh dấu mục tiêu đã hoàn thành
11. Xóa mục tiêu học tập
12. Thống kê tiến độ học tập
13. Thêm ghi chú cho môn học
14. Xem ghi chú của môn học
15. Xóa ghi chú khỏi môn học
16. Tìm kiếm môn học theo tên
17. Tìm kiếm tài liệu theo từ khóa
18. Xuất báo cáo kế hoạch học tập ra file
19. Lưu kế hoạch học tập vào file
20. Tải kế hoạch học tập từ file
0. Thoát chương trình
=====================
"""

clear_screen()
print(menu_text)

while True:
    choice = input("\nChọn chức năng: ").strip()
    if choice == "0":
        save_to_file()
        print("Đã lưu và thoát.")
        break
    func = menu.get(choice)
    if func:
        result = func()
        if result: print(result)
    else:
        print("Chức năng không hợp lệ.")