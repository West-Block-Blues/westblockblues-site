import os

from jinja2 import Environment, FileSystemLoader, Template
import mistune
import yaml


target_folder = "site/"
content_folder = "content/"
template_folder = "templates/"

# defs
teams = {
  "atkmb": "ATK Mohun Bagan",
  "bfc": "Bengaluru FC",
  "cfc": "Chennaiyin FC",
  "ebfc": "East Bengal FC",
  "fcg": "FC Goa",
  "hfc": "Hyderabad FC",
  "jfc": "Jamshedpur FC",
  "kbfc": "Kerala Blasters FC",
  "mcfc": "Mumbai City FC",
  "neufc": "NorthEast United FC",
  "ofc": "Odisha FC",
}
venues = [
  ["GMC Athletic Stadium", "Bambolim, Goa"], #0
  ["Tilak Maidan Stadium", "Vasco da Gama, Goa"], #1
]

# load templates
templates = {}
for template_file in os.listdir(template_folder):
  with open(template_folder+template_file) as f:
    templates[template_file] = Environment(loader=FileSystemLoader(template_folder)).from_string(f.read())
    f.close()

# generate pages
for page_file in os.listdir(content_folder):
  print(page_file)
  contents = ""
  with open(content_folder+page_file) as f:
    contents = f.read().split("---")
    f.close()
  context = yaml.safe_load(contents[0])
  context["body"] = mistune.markdown(contents[1], escape=False)
  context["teams"] = teams
  context["venues"] = venues
  rendered_page = templates[context["template"]].render(**context)
  path = target_folder + context["target"]
  os.makedirs(os.path.dirname(path), exist_ok=True)
  with open(path, "w") as f:
    f.write(rendered_page)
    f.close()  
  
