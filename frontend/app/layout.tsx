import type { Metadata, Viewport } from 'next';
import {Inter,Noto_Sans_Telugu,Noto_Sans_Devanagari} from 'next/font/google';
import './globals.css';
import './polish.css';
const inter=Inter({subsets:['latin'],weight:['400','600'],display:'optional',variable:'--font-inter',preload:true});
const telugu=Noto_Sans_Telugu({subsets:['telugu'],weight:['400','600'],display:'optional',variable:'--font-telugu',preload:true});
const hindi=Noto_Sans_Devanagari({subsets:['devanagari'],weight:['400','600'],display:'optional',variable:'--font-hindi',preload:true});
export const metadata: Metadata = { title: 'Sahi GST — Invoice clarity. Business confidence.', description: 'Review invoices, understand mismatches and prepare supplier correction requests in one workspace.', manifest: '/manifest.webmanifest' };
export const viewport: Viewport = { themeColor: '#0F2A44' };
export default function RootLayout({ children }: Readonly<{children: React.ReactNode}>) { return <html lang="en" className={`${inter.variable} ${telugu.variable} ${hindi.variable}`}><body>{children}</body></html>; }
