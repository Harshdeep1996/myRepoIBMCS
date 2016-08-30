import jinja2

#String template
templateObj = jinja2.Template('Hello {{firstName}}!, my surname is {{surname}}') #Making a template object
print templateObj.render(firstName="Harshdeep",surname="Harshdeep") # Returns the result in unicode and pass in the dictionary

#Difference between trim_blocks and non trim blocks
#What is the difference between use and no use of lstrip_blocks?
template2 = '''<div>
			{% if x % 5 == 0 %}
			<small>{{ x }}</small>
			{% endif -%}
			</div>
			'''

template1 = jinja2.Template(template2)
template2 = jinja2.Template(template2, trim_blocks =True,lstrip_blocks=True)

print template1.render(x=3)
print '\n<!-- {} -->\n'.format('-' * 32)
print template2.render(x=5)

# + -  SPACING PRACTICE
seq = [1,2,3,4,5,6,7,8,9]
template3 = '''
				<ul>
				{% for item in seq -%}
					{{ item }}
			    {%- endfor %}
			    </ul>
			'''

template3 = jinja2.Template(template3)
print template3.render(seq=seq)

#Marking the snippet of code as raw, which is it won't be under the jurisdiction of JINJA
#the whole raw thing gets printed out on the screen
template4 = '''
				{% raw %}
				<ul>
    				{% for item in seq %}
        				<li>{{ item }}</li>
    				{% endfor %}
    			</ul>
				{% endraw %}
			'''

template4 = jinja2.Template(template4)
print template4.render(seq=seq)

#



