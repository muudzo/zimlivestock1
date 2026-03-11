import { useQuery } from 'react-query';
import { livestockAPI } from '@/services/api';

export const useLivestock = (category?: string) => {
    const { data, isLoading, error, refetch } = useQuery(
        ['livestock', category],
        () => livestockAPI.getListings({ category }),
        {
            staleTime: 5 * 60 * 1000,
            retry: 2,
        }
    );

    return {
        items: data?.data || [],
        isLoading,
        error,
        refetch,
    };
};
