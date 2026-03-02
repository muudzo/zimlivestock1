import { useEffect, useState } from 'react';
import { paymentAPI } from '@/services/api';
import { toast } from 'sonner';

interface PaymentStatusProps {
    reference: string;
}

export function PaymentStatus({ reference }: PaymentStatusProps) {
    const [status, setStatus] = useState<any>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchStatus = async () => {
            try {
                const data = await paymentAPI.getStatus(reference);
                setStatus(data);
            } catch (err: any) {
                console.error('Failed to fetch payment status', err);
                toast.error('Could not get payment status.');
            } finally {
                setLoading(false);
            }
        };
        fetchStatus();
    }, [reference]);

    if (loading) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <div className="text-center">
                    <div className="w-8 h-8 border-4 border-primary border-t-transparent animate-spin mx-auto mb-4" />
                    <p className="text-muted-foreground">Checking payment...</p>
                </div>
            </div>
        );
    }

    if (!status) {
        return <p className="text-center p-4">No payment information available.</p>;
    }

    return (
        <div className="min-h-screen flex items-center justify-center p-4">
            <div className="max-w-md w-full bg-white shadow rounded-lg p-6 text-center">
                <h2 className="text-xl font-semibold mb-4">Payment {status.paid ? 'Success' : 'Status'}</h2>
                <p className="mb-2">Reference: {status.reference}</p>
                <p className="mb-4">Current status: {status.status}</p>
                {status.redirect_url && (
                    <p>
                        <a href={status.redirect_url} className="text-primary underline">
                            Complete payment in browser
                        </a>
                    </p>
                )}
                {status.instructions && (
                    <p className="mt-2">{status.instructions}</p>
                )}
            </div>
        </div>
    );
}
