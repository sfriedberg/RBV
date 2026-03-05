import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "DT2216 + Paclitaxel — How They Kill Cancer Cells",
  description:
    "An animated guide to understanding how Dialectic Therapeutics' DT2216 PROTAC degrader works with paclitaxel to restore apoptosis in cancer cells.",
  openGraph: {
    title: "DT2216 + Paclitaxel — How They Kill Cancer Cells",
    description:
      "An animated guide to apoptosis, BCL-XL degradation, and next-generation cancer therapy.",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        {children}
      </body>
    </html>
  );
}
