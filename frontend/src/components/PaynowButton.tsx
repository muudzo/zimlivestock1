import { Button } from './ui/button';

interface PaynowButtonProps {
    onClick: (e: React.MouseEvent) => void;
    className?: string;
    disabled?: boolean;
}

export function PaynowButton({ onClick, className, disabled }: PaynowButtonProps) {
    return (
        <Button
            onClick={onClick}
            disabled={disabled}
            className={`relative overflow-hidden group h-11 transition-all duration-300 hover:shadow-lg active:scale-95 border-none p-0 ${className}`}
            style={{
                backgroundColor: '#005a9c', // Official Paynow Blue
                minWidth: '200px'
            }}
        >
            <div className="absolute inset-0 bg-gradient-to-r from-white/0 via-white/10 to-white/0 translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-1000" />
            <div className="flex items-center justify-center w-full h-full px-6">
                <img
                    src="/paynow-button.png"
                    alt="Pay with Paynow"
                    className="h-7 w-auto object-contain brightness-0 invert"
                />
                <span className="ml-3 font-semibold text-white tracking-wide">
                    Pay with Paynow
                </span>
            </div>
        </Button>
    );
}
