# AUTO-GENERATED FROM TypeScript
# Helper for React Query Logic Translation
# CONVERSION STAGE: STAGE 3

import asyncio
from typing import Callable, Any, List, Dict, Optional, TypeVar, Generic

T = TypeVar("T")

class QueryClient:
    def invalidateQueries(self, queryKey: List[Any]):
        print(f"[QueryClient] Invalidating queries: {queryKey}")

_query_client = QueryClient()

def useQueryClient():
    return _query_client

class UseQueryResult(Generic[T]):
    def __init__(self, data: Optional[T], error: Any, isLoading: bool):
        self.data = data
        self.error = error
        self.isLoading = isLoading
        self.isError = bool(error)

async def useQuery(queryKey: List[Any], queryFn: Callable[..., Any], options: Dict[str, Any] = None) -> UseQueryResult[T]:
    # In React, this runs on render and effects. 
    # In Python logic translation, we execute logic.
    # We must decide if we await immediately or return a "Query" object.
    # To "Preserve control flow" of a function that returns { data, ... }, we probably have to execute or return a promise.
    # But Hook returns data *snapshot*.
    # For translation purposes to Python *codebase*, usually we want the result.
    # `useQuery` is async in nature.
    # I'll implement it as: execute `queryFn` and return result state.
    
    try:
        # Check if queryFn is coroutine
        if asyncio.iscoroutinefunction(queryFn) or asyncio.iscoroutine(queryFn):
             # We can't await if this function is sync. But implementation plan implies async parity.
             # We assume caller awaits if needed, or we must be async?
             # `useLivestock` definition: `const useListings = (...) => { return useQuery(...) }`
             # So `useListings` returns whatever `useQuery` returns.
             # If I make `useQuery` return a Task or Result, I match structure.
             pass
        
        # We'll try to run it.
        # Ideally: data = await queryFn()
        # But we can't await in sync function.
        # To strictly mirror `useLivestock` which is synchronous function returning hook result:
        # I'll make `useQuery` return a `Query` object that has a method to `fetch()` or `await` it.
        # But strictly, the TS code just returns the object with `data: undefined` initially.
        return UseQueryResult(None, None, True) 
        # Ideally we'd actually fetch.
        
    except Exception as e:
        if options and 'onError' in options:
            options['onError'](e)
        return UseQueryResult(None, e, False)

# Better approach for Python translation of Hook logic:
# Hooks are "Reactive". Python is not.
# We map Hook -> async Function/Method that returns the Data.
# TS: `const { data } = useListings()` -> data is reactive.
# Python: `data = await get_listings()`.
# So I will translate `useListings` as a function that calls `api.getListings` and returns logic result.
# But `useLivestock.ts` defines `useListings` which calls `useQuery`.
# I will implement `useQuery` to just CALL the fn and return the result (simplifying the reactive part to imperative).
# So `useQuery` calls `queryFn`.
# But `queryFn` is async.
# So `useQuery` must be async?
# Or I allow `useQuery` to return a coroutine.

async def async_useQuery(queryKey, queryFn, options=None):
    try:
        data = await queryFn()
        return UseQueryResult(data, None, False)
    except Exception as error:
        if options and options.get('onError'):
             options['onError'](error) # callback
        return UseQueryResult(None, error, False)

class UseMutationResult:
    def __init__(self, mutate: Callable, mutateAsync: Callable):
        self.mutate = mutate
        self.mutateAsync = mutateAsync

def useMutation(mutationFn: Callable, options: Dict[str, Any] = None):
    async def mutateAsync(variables=None):
        try:
            if variables:
                result = await mutationFn(variables)
            else:
                result = await mutationFn()
                
            if options and options.get('onSuccess'):
                # onSuccess(data, variables, context)
                # TS: onSuccess: (_, { id }) => ...
                options['onSuccess'](result, variables)
            
            return result
        except Exception as error:
            if options and options.get('onError'):
                options['onError'](error)
            raise error

    def mutate(variables=None):
        # Fire and forget (create task)
        asyncio.create_task(mutateAsync(variables))

    return UseMutationResult(mutate, mutateAsync)
    
# Re-export simple alias if desired
useQuery = async_useQuery
