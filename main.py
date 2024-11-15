import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw, ImageTk
import requests

PLATE_RECOGNIZER_API_URL = "https://api.platerecognizer.com/v1/plate-reader/"
PLATE_RECOGNIZER_API_KEY = "PLATE_RECOGNIZER_API_KEY"  

def process_image(image_path):
    try:
        with open(image_path, "rb") as image_file:
            response = requests.post(
                PLATE_RECOGNIZER_API_URL,
                headers={"Authorization": f"Token {PLATE_RECOGNIZER_API_KEY}"},
                files={"upload": image_file}
            )

        if response.status_code in [200, 201]:
            result = response.json()
            
            if "results" in result and result["results"]:
                plate = result["results"][0].get("plate", "").strip()
                box = result["results"][0].get("box", None)
                return plate.upper(), box
            else:
                return "No license plate detected.", None
        else:
            return f"API Error: {response.status_code}, {response.text}", None
    except Exception as e:
        return f"Error processing image: {str(e)}", None

def fetch_car_details(number_plate):
    try:
        api_url = "https://driver-vehicle-licensing.api.gov.uk/vehicle-enquiry/v1/vehicles"
        headers = {
            "x-api-key": "ENTER_DVLA_API_KEY_HERE",
            "Content-Type": "application/json"
        }
        data = {"registrationNumber": number_plate.upper().replace(" ", "").replace("-", "")}
        response = requests.post(api_url, headers=headers, json=data)

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return {"error": "Vehicle not found in DVLA database."}
        else:
            return {"error": f"API Error: {response.status_code}, {response.text}"}
    except Exception as e:
        return {"error": str(e)}

def draw_box_on_image(image_path, box, max_width=400):
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    if box:
        draw.rectangle(
            [box["xmin"], box["ymin"], box["xmax"], box["ymax"]],
            outline="red",
            width=20
        )
    width_percent = max_width / float(image.width)
    new_height = int(float(image.height) * width_percent)
    resized_image = image.resize((max_width, new_height), Image.Resampling.LANCZOS)
    return resized_image

def upload_and_process():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
    if file_path:
        extracted_plate, box = process_image(file_path)
        if extracted_plate.startswith("Error"):
            messagebox.showerror("Error", extracted_plate)
        elif extracted_plate == "No license plate detected.":
            messagebox.showinfo("Result", "No license plate detected in the image.")
        else:
            number_plate_var.set(extracted_plate)
            
            image_with_box = draw_box_on_image(file_path, box)
            tk_image = ImageTk.PhotoImage(image_with_box)
            image_label.config(image=tk_image)
            image_label.image = tk_image

            if test_mode.get():
                details_text.set(f"Test Mode: Registration Number is {extracted_plate}")
            else:
                car_details = fetch_car_details(extracted_plate)
                if "error" in car_details:
                    messagebox.showerror("API Error", car_details["error"])
                else:
                    formatted_details = "\n".join(
                        [f"{key.capitalize()}: {value}" for key, value in car_details.items()]
                    )
                    details_text.set(formatted_details)

def style_button(button):
    button.config(
        bg="#444",
        fg="white",
        font=("Arial", 12, "bold"),
        relief="flat",
        highlightthickness=0,
        bd=0,
        padx=15,
        pady=5
    )
    button.bind("<Enter>", lambda e: button.config(bg="#666"))
    button.bind("<Leave>", lambda e: button.config(bg="#444"))

app = tk.Tk()
app.title("Find Car Details - Otto :D")
app.geometry("900x600")
app.config(bg="#222")

main_frame = tk.Frame(app, bg="#222")
main_frame.pack(fill="both", expand=True, padx=10, pady=10)

left_frame = tk.Frame(main_frame, width=450, height=600, bg="#222")
left_frame.pack(side="left", padx=10, pady=10, fill="y")

right_frame = tk.Frame(main_frame, width=450, height=600, bg="#222")
right_frame.pack(side="right", padx=10, pady=10, fill="y")

top_frame = tk.Frame(app, bg="#222")
top_frame.pack(fill="x", pady=10)

test_mode = tk.BooleanVar(value=False)
tk.Checkbutton(
    top_frame, text="Test Mode (do not send to API)", variable=test_mode, font=("Arial", 12), bg="#222", fg="white",
    selectcolor="#444"
).pack(side="left", padx=10)

upload_button = tk.Button(top_frame, text="Upload Image", command=upload_and_process)
style_button(upload_button)
upload_button.pack(side="right", padx=10)

image_label = tk.Label(left_frame, bg="#333")
image_label.pack()

details_label = tk.Label(right_frame, text="Car Details", font=("Arial", 16, "bold"), bg="#222", fg="white")
details_label.pack(pady=10)

details_text = tk.StringVar()
details_output = tk.Label(
    right_frame, textvariable=details_text, font=("Arial", 12), justify="left", wraplength=350, bg="#222", fg="white"
)
details_output.pack(pady=10)

number_plate_var = tk.StringVar()
plate_label = tk.Label(right_frame, text="Extracted Number Plate:", font=("Arial", 14, "bold"), bg="#222", fg="white")
plate_label.pack(pady=5)
plate_entry = tk.Entry(right_frame, textvariable=number_plate_var, state="readonly", width=30, bg="#444", fg="white", font=("Arial", 12), relief="flat")
plate_entry.pack(pady=5)

app.mainloop()
