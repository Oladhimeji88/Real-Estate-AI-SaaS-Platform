import "./globals.css";
import type { ReactNode } from "react";

export const metadata = {
  title: "RealEstate Intelligence Suite",
  description: "AI SaaS for listings intelligence and market analytics"
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
