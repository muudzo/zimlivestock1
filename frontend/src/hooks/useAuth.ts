import { useAuthStore } from '../stores/authStore';

export const useAuth = () => {
    const store = useAuthStore();

    return {
        ...store,
        // Add any derived state or additional logic here
    };
};
