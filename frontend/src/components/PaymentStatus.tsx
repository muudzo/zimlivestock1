import { useEffect, useState } from 'react';
import { paymentAPI } from '@/services/api';
import { toast } from 'sonner';
import { Button } from './ui/button';
import { ArrowLeft, CheckCircle2, AlertCircle, Clock } from 'lucide-react';

interface PaymentStatusProps {
    reference: string;
    onBack: () => void;
}

export function PaymentStatus({ reference, onBack }: PaymentStatusProps) {
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

    const isPaid = status.paid || status.status?.toLowerCase() === 'paid';

    return (
        <div className="min-h-screen flex items-center justify-center p-4 bg-muted/30">
            <div className="max-w-md w-full bg-card shadow-xl rounded-2xl p-8 text-center animate-in fade-in zoom-in duration-300">
                <div className="flex justify-center mb-6">
                    {isPaid ? (
                        <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center">
                            <CheckCircle2 className="w-10 h-10 text-green-600" />
                        </div>
                    ) : status.status?.toLowerCase() === 'cancelled' ? (
                        <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center">
                            <AlertCircle className="w-10 h-10 text-red-600" />
                        </div>
                    ) : (
                        <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center">
                            <Clock className="w-10 h-10 text-blue-600" />
                        </div>
                    )}
                </div>

                <h2 className="text-2xl font-bold mb-2">
                    Payment {isPaid ? 'Successful' : status.status || 'Status'}
                </h2>

                <div className="space-y-4 my-6">
                    <div className="bg-muted p-3 rounded-lg text-sm font-mono break-all text-muted-foreground">
                        Ref: {status.reference}
                    </div>

                    <p className="text-muted-foreground">
                        {isPaid
                            ? 'Your transaction has been confirmed. Thank you for your purchase!'
                            : 'We are still processing your request or waiting for confirmation.'}
                    </p>

                    {status.redirect_url && !isPaid && (
                        <Button asChild className="w-full">
                            <a href={status.redirect_url}>
                                Complete in Browser
                            </a>
                        </Button>
                    )}

                    {status.instructions && (
                        <div className="bg-blue-50 border border-blue-100 p-4 rounded-xl text-blue-800 text-sm italic">
                            {status.instructions}
                        </div>
                    )}
                </div>

                <Button variant="outline" className="w-full mt-4" onClick={onBack}>
                    <ArrowLeft className="w-4 h-4 mr-2" />
                    Back to Marketplace
                </Button>
            </div>
        </div>
    );
}
