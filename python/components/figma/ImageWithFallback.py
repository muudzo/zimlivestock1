# AUTO-GENERATED FROM TypeScript
# SOURCE: components/figma/ImageWithFallback.tsx
# CONVERSION STAGE: STAGE 3
# DO NOT MODIFY LOGIC WITHOUT COMPARING TO ORIGINAL

from src.lib.react import React, jsx

ERROR_IMG_SRC = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iODgiIGhlaWdodD0iODgiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgc3Ryb2tlPSIjMDAwIiBzdHJva2UtbGluZWpvaW49InJvdW5kIiBvcGFjaXR5PSIuMyIgZmlsbD0ibm9uZSIgc3Ryb2tlLXdpZHRoPSIzLjciPjxyZWN0IHg9IjE2IiB5PSIxNiIgd2lkdGg9IjU2IiBoZWlnaHQ9IjU2IiByeD0iNiIvPjxwYXRoIGQ9Im0xNiA1OCAxNi0xOCAzMiAzMiIvPjxjaXJjbGUgY3g9IjUzIiBjeT0iMzUiIHI9IjciLz48L3N2Zz4KCg=='

def ImageWithFallback(props):
    # const [didError, setDidError] = useState(false)
    didError = False
    def setDidError(val): pass

    # const handleError = () => { setDidError(true) }
    def handleError():
        nonlocal didError # Logic representation
        didError = True
        setDidError(True)

    # const { src, alt, style, className, ...rest } = props
    src = props.get('src')
    alt = props.get('alt')
    style = props.get('style')
    className = props.get('className')
    rest = {k: v for k, v in props.items() if k not in ['src', 'alt', 'style', 'className']}

    if didError:
        return jsx('div', {
            'className': f"inline-block bg-gray-100 text-center align-middle {className or ''}",
            'style': style
        },
            jsx('div', {'className': "flex items-center justify-center w-full h-full"},
                jsx('img', {
                    'src': ERROR_IMG_SRC,
                    'alt': "Error loading image",
                    **rest,
                    'data-original-url': src
                })
            )
        )
    else:
        return jsx('img', {
            'src': src,
            'alt': alt,
            'className': className,
            'style': style,
            'onError': handleError,
            **rest
        })
