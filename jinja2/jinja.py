from jinja2 import Template

templateObj = Template('Hello {{firstName}}!, my surname is {{surname}}') #Making a template object
print templateObj.render(firstName="Harshdeep",surname="Harshdeep") # Returns the result in unicode and pass in the dictionary