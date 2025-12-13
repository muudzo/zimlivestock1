# AUTO-GENERATED FROM TypeScript
# React Mock
# CONVERSION STAGE: STAGE 3

class React:
    @staticmethod
    def createElement(component, props=None, *children):
        return {
            'type': component,
            'props': props or {},
            'children': children
        }

    class Component:
        def __init__(self, props):
            self.props = props

    @staticmethod
    def useState(initial):
        # Mock hook
        return [initial, lambda x: None]

    @staticmethod
    def useEffect(effect, deps=None):
        pass
        
    @staticmethod
    def StrictMode(children):
        return {'type': 'StrictMode', 'children': children}

default = React

# JSX helper
# We will translate <Div /> to React.createElement('Div', ...)
# Or just a `jsx` function
def jsx(tag, props=None, *children):
    return React.createElement(tag, props, *children)
