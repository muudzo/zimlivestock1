# AUTO-GENERATED FROM TypeScript
# SOURCE: src/main.tsx
# CONVERSION STAGE: STAGE 3
# DO NOT MODIFY LOGIC WITHOUT COMPARING TO ORIGINAL

import os
import json
from src.lib.react import React, default as ReactDefault, jsx
from src.lib.react_query import QueryClient, useQueryClient
# from src.lib.react_error_boundary import ErrorBoundary # TODO
# from src.lib.react_helmet_async import HelmetProvider # TODO
# from src.lib.sonner import Toaster # Mocked
# import App from '../App'
from src.services.api import localStorage, window, document

# Placeholders for missing modules that are not yet translated
try:
    from App import App
except ImportError:
    App = lambda: jsx('App')

# Create a client
# const queryClient = new QueryClient(...)
# In our mock, QueryClient is singleton or just class.
# TS initializes it with defaults.
class QueryClientConfig:
    def __init__(self, config):
        self.config = config

queryClientConfig = QueryClientConfig({
  'defaultOptions': {
    'queries': {
      'retry': 1,
      'refetchOnWindowFocus': False,
      'staleTime': 5 * 60 * 1000, # 5 minutes
    },
    'mutations': {
      'retry': 1,
    },
  },
})

# Error Fallback Component
def ErrorFallback(props):
    error = props['error']
    resetErrorBoundary = props['resetErrorBoundary']
    
    return jsx('div', {'className': "min-h-screen flex items-center justify-center bg-background p-4"},
      jsx('div', {'className': "text-center space-y-4 max-w-md"},
        jsx('div', {'className': "w-16 h-16 mx-auto bg-destructive/10 rounded-full flex items-center justify-center"},
          jsx('span', {'className': "text-2xl"}, "⚠️")
        ),
        jsx('h2', {'className': "text-xl font-semibold"}, "Something went wrong"),
        jsx('p', {'className': "text-muted-foreground text-sm"},
          "We're sorry, but something unexpected happened. Please try refreshing the page."
        ),
        jsx('div', {'className': "space-y-2"},
          jsx('button', {
            'onClick': resetErrorBoundary,
            'className': "w-full bg-primary text-primary-foreground px-4 py-2 rounded-md hover:bg-primary/90 transition-colors"
          }, "Try again"),
          jsx('button', {
            'onClick': lambda: window.location.reload(), # Mock reload
            'className': "w-full bg-secondary text-secondary-foreground px-4 py-2 rounded-md hover:bg-secondary/80 transition-colors"
          }, "Refresh page")
        ),
        # {process.env['NODE_ENV'] === 'development' && ...}
        jsx('details', {'className': "text-left text-xs text-muted-foreground"},
             jsx('summary', {'className': "cursor-pointer"}, "Error details"),
             jsx('pre', {'className': "mt-2 p-2 bg-muted rounded text-xs overflow-auto"},
               error.message if hasattr(error, 'message') else str(error)
             )
        ) if os.environ.get('NODE_ENV') == 'development' else None
      )
    )

# Initialize theme on app start
def initializeTheme():
    # const savedTheme = localStorage.getItem('app-storage')
    savedTheme = localStorage.getItem('app-storage')
    if savedTheme:
        try:
            # const { theme } = JSON.parse(savedTheme)
            parsed = json.loads(savedTheme)
            # In persist middleware, it's { state: { theme: ... } } usually
            # But the TS code code says `const { theme } = JSON.parse`.
            # If the storage format is exactly { theme: ... }, then this works.
            # But zustand persist usually wraps it.
            # "Mirror TS behavior": TS code assumes `JSON.parse(savedTheme)` has `theme` property directly?
            # Or destructuring `{ theme } = ...`.
            # If persist stores `{ state: { theme: ... } }`, then `{ theme }` extraction would fail or be undefined unless strictly typed.
            # We will strictly replicate TS:
            # `const { theme } = ...` means accessing property `theme`.
            theme = parsed.get('theme')
            
            # if (theme === 'dark' || (theme === 'system' && window.matchMedia('(prefers-color-scheme: dark)').matches))
            is_dark = False
            if theme == 'dark':
                is_dark = True
            elif theme == 'system':
                # window.matchMedia mock
                is_dark = False 
            
            if is_dark:
                document.documentElement.classList.add('dark')
            else:
                document.documentElement.classList.remove('dark')
        except Exception as error:
            print(f'Failed to parse theme from localStorage: {error}')

# Initialize theme
initializeTheme()

# ReactDOM.createRoot(document.getElementById('root')!).render(...)
# In python we just define the main execution
def main():
    root_element = document.getElementById('root') # Mock needed? document doesn't have getElementById in our simple mock
    # We ignore standard DOM methods for now or assume they run
    
    app_tree = jsx('React.StrictMode', {},
        jsx('ErrorBoundary', {'FallbackComponent': ErrorFallback},
            jsx('QueryClientProvider', {'client': queryClientConfig}, # Pass config as client? mock
                jsx('HelmetProvider', {},
                    jsx(App, {}),
                    jsx('Toaster', {
                        'position': "top-right",
                        'richColors': True, # boolean prop
                        'closeButton': True,
                        'duration': 4000,
                        'toastOptions': {
                            'style': {
                                'background': 'hsl(var(--background))',
                                'color': 'hsl(var(--foreground))',
                                'border': '1px solid hsl(var(--border))',
                            },
                        }
                    }),
                    jsx('ReactQueryDevtools', {'initialIsOpen': False}) if os.environ.get('NODE_ENV') == 'development' else None
                )
            )
        )
    )
    return app_tree

if __name__ == "__main__":
    main()
