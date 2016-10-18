import nose
from compliance.utils.controls import ControlValidation

if __name__ == '__main__':
    nose.main(addplugins=[ControlValidation()])
