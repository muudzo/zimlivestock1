import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
    return twMerge(clsx(inputs));
}

export function formatCurrency(amount: number, currency: string = "USD") {
    return new Intl.NumberFormat("en-ZW", {
        style: "currency",
        currency: currency,
        minimumFractionDigits: 0,
        maximumFractionDigits: 0,
    }).format(amount);
}

export function formatCurrencyCompact(amount: number, currency: string = "USD") {
    return new Intl.NumberFormat("en-ZW", {
        style: "currency",
        currency: currency,
        notation: "compact",
        maximumFractionDigits: 1,
    }).format(amount);
}

export function getCategoryIcon(category: string): string {
    const icons: Record<string, string> = {
        cattle: "🐄",
        goats: "🐐",
        sheep: "🐑",
        pigs: "🐷",
        chickens: "🐔",
        horses: "🐎",
        donkeys: "🦙",
    };
    return icons[category] || "🐄";
}

export function formatTimeLeft(endDate: Date | string): string {
    const end = typeof endDate === "string" ? new Date(endDate) : endDate;
    const now = new Date();

    if (end.getTime() <= now.getTime()) {
        return "Ended";
    }

    const diffMs = end.getTime() - now.getTime();
    const days = Math.floor(diffMs / (1000 * 60 * 60 * 24));
    const hours = Math.floor((diffMs % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((diffMs % (1000 * 60 * 60)) / (1000 * 60));

    if (days > 0) {
        return `${days}d ${hours}h`;
    } else if (hours > 0) {
        return `${hours}h ${minutes}m`;
    } else {
        return `${minutes}m`;
    }
}
