# AUTO-GENERATED FROM TypeScript
# SOURCE: src/hooks/useLivestock.ts
# CONVERSION STAGE: STAGE 3
# DO NOT MODIFY LOGIC WITHOUT COMPARING TO ORIGINAL

import asyncio
from typing import Dict, Any, Optional, List

try:
    from src.lib.react_query import useQuery, useMutation, useQueryClient
    from src.services.api import livestockAPI, biddingAPI, mockAPI
    from src.lib.sonner import toast
    from src.types.index import FilterOptions
except ImportError:
    # Fallbacks for dev without full env
    useQuery = lambda k, f, o=None: None
    useMutation = lambda f, o=None: None
    useQueryClient = lambda: None
    livestockAPI = None
    biddingAPI = None
    mockAPI = None
    toast = None
    FilterOptions = dict

def useLivestock():
    queryClient = useQueryClient()

    # Get all listings
    def useListings(filters: Optional[dict] = None, page: int = 1, limit: int = 10):
        # queryKey = ['livestock', filters, page, limit]
        queryKey = ['livestock', filters, page, limit]
        
        # fn = () => livestockAPI.getListings({ ...filters, page, limit })
        async def fetcher():
            params = {}
            if filters: params.update(filters)
            params['page'] = page
            params['limit'] = limit
            return await livestockAPI.getListings(params)
            
        return useQuery(
            queryKey,
            fetcher,
            {
                'staleTime': 5 * 60 * 1000,
                'cacheTime': 10 * 60 * 1000,
                'retry': 2,
                'onError': lambda error: (
                    print(f'Failed to fetch listings: {error}'),
                    toast.error('Failed to load listings')
                )
            }
        )

    # Get single listing
    def useListing(id: str):
        return useQuery(
            ['livestock', id],
            lambda: livestockAPI.getListing(id),
            {
                'enabled': bool(id),
                'staleTime': 2 * 60 * 1000,
                'cacheTime': 5 * 60 * 1000,
                'retry': 2,
                'onError': lambda error: (
                    print(f'Failed to fetch listing: {error}'),
                    toast.error('Failed to load listing details')
                )
            }
        )

    # Get my listings
    def useMyListings():
        return useQuery(
            ['livestock', 'my-listings'],
            lambda: livestockAPI.getMyListings(),
            {
                'staleTime': 2 * 60 * 1000,
                'cacheTime': 5 * 60 * 1000,
                'retry': 2,
                'onError': lambda error: (
                    print(f'Failed to fetch my listings: {error}'),
                    toast.error('Failed to load your listings')
                )
            }
        )

    # Search listings
    def useSearchListings(query: str, filters: Optional[dict] = None):
        return useQuery(
            ['livestock', 'search', query, filters],
            lambda: livestockAPI.searchListings(query, filters),
            {
                'enabled': bool(query.strip()),
                'staleTime': 2 * 60 * 1000,
                'cacheTime': 5 * 60 * 1000,
                'retry': 2,
                'onError': lambda error: (
                    print(f'Failed to search listings: {error}'),
                    toast.error('Search failed')
                )
            }
        )

    # Create listing mutation
    def useCreateListing():
        return useMutation(
            lambda listingData: livestockAPI.createListing(listingData),
            {
                'onSuccess': lambda data, vars: (
                    queryClient.invalidateQueries(['livestock']),
                    toast.success('Listing created successfully!')
                ),
                'onError': lambda error: (
                    print(f'Failed to create listing: {error}'),
                    toast.error('Failed to create listing')
                )
            }
        )

    # Update listing mutation
    def useUpdateListing():
        # MutationFn: ({ id, data }) => ...
        # Vars in python are passed as arg. Expecting dict here matching TS signature proxy?
        # Python mutation executes fn(variables).
        # We expect variables to be { 'id': ..., 'data': ... }
        return useMutation(
            lambda variables: livestockAPI.updateListing(variables['id'], variables['data']),
            {
                'onSuccess': lambda data, variables: (
                    queryClient.invalidateQueries(['livestock', variables['id']]),
                    queryClient.invalidateQueries(['livestock', 'my-listings']),
                    toast.success('Listing updated successfully!')
                ),
                'onError': lambda error: (
                    print(f'Failed to update listing: {error}'),
                    toast.error('Failed to update listing')
                )
            }
        )

    # Delete listing mutation
    def useDeleteListing():
        return useMutation(
            lambda id: livestockAPI.deleteListing(id),
            {
                'onSuccess': lambda data, vars: (
                    queryClient.invalidateQueries(['livestock']),
                    queryClient.invalidateQueries(['livestock', 'my-listings']),
                    toast.success('Listing deleted successfully!')
                ),
                'onError': lambda error: (
                    print(f'Failed to delete listing: {error}'),
                    toast.error('Failed to delete listing')
                )
            }
        )

    # Upload image mutation
    def useUploadImage():
        return useMutation(
             lambda file: livestockAPI.uploadImage(file),
             {
                 'onError': lambda error: (
                     print(f'Failed to upload image: {error}'),
                     toast.error('Failed to upload image')
                 )
             }
        )

    return {
        'useListings': useListings,
        'useListing': useListing,
        'useMyListings': useMyListings,
        'useSearchListings': useSearchListings,
        'useCreateListing': useCreateListing,
        'useUpdateListing': useUpdateListing,
        'useDeleteListing': useDeleteListing,
        'useUploadImage': useUploadImage
    }


def useBidding():
    queryClient = useQueryClient()

    def useBidHistory(livestockId: str):
        return useQuery(
            ['bids', livestockId],
            lambda: biddingAPI.getBidHistory(livestockId),
            {
                'enabled': bool(livestockId),
                'staleTime': 30 * 1000,
                'cacheTime': 2 * 60 * 1000,
                'retry': 2,
                'onError': lambda error: (
                    print(f'Failed to fetch bid history: {error}'),
                    toast.error('Failed to load bid history')
                )
            }
        )

    def useMyBids():
        return useQuery(
            ['bids', 'my-bids'],
            lambda: biddingAPI.getMyBids(),
            {
                'staleTime': 60 * 1000,
                'cacheTime': 5 * 60 * 1000,
                'retry': 2,
                'onError': lambda error: (
                    print(f'Failed to fetch my bids: {error}'),
                    toast.error('Failed to load your bids')
                )
            }
        )

    def usePlaceBid():
        # Vars: { livestockId: str, amount: number }
        return useMutation(
            lambda vars: biddingAPI.placeBid(vars['livestockId'], vars['amount']),
            {
                'onSuccess': lambda data, vars: (
                     queryClient.invalidateQueries(['bids', vars['livestockId']]),
                     queryClient.invalidateQueries(['bids', 'my-bids']),
                     queryClient.invalidateQueries(['livestock', vars['livestockId']]),
                     toast.success('Bid placed successfully!')
                ),
                'onError': lambda error: (
                    print(f'Failed to place bid: {error}'),
                    toast.error('Failed to place bid')
                )
            }
        )

    def useRetractBid():
        return useMutation(
            lambda bidId: biddingAPI.retractBid(bidId),
            {
                'onSuccess': lambda data, vars: (
                    queryClient.invalidateQueries(['bids']),
                    queryClient.invalidateQueries(['bids', 'my-bids']),
                    toast.success('Bid retracted successfully!')
                ),
                'onError': lambda error: (
                    print(f'Failed to retract bid: {error}'),
                    toast.error('Failed to retract bid')
                )
            }
        )

    return {
        'useBidHistory': useBidHistory,
        'useMyBids': useMyBids,
        'usePlaceBid': usePlaceBid,
        'useRetractBid': useRetractBid
    }


def useMockLivestock():
    async def fetcher():
        # Promise.resolve(...)
        return mockAPI.getMockListings()

    return useQuery(
        ['livestock', 'mock'],
        fetcher,
        {
            'staleTime': float('inf'),
            'cacheTime': float('inf')
        }
    )
