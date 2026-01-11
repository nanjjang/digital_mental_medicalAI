
// this file is generated — do not edit it


declare module "svelte/elements" {
	export interface HTMLAttributes<T> {
		'data-sveltekit-keepfocus'?: true | '' | 'off' | undefined | null;
		'data-sveltekit-noscroll'?: true | '' | 'off' | undefined | null;
		'data-sveltekit-preload-code'?:
			| true
			| ''
			| 'eager'
			| 'viewport'
			| 'hover'
			| 'tap'
			| 'off'
			| undefined
			| null;
		'data-sveltekit-preload-data'?: true | '' | 'hover' | 'tap' | 'off' | undefined | null;
		'data-sveltekit-reload'?: true | '' | 'off' | undefined | null;
		'data-sveltekit-replacestate'?: true | '' | 'off' | undefined | null;
	}
}

export {};


declare module "$app/types" {
	export interface AppTypes {
		RouteId(): "/" | "/business" | "/chat" | "/checkin" | "/consent" | "/download" | "/features" | "/goals" | "/history" | "/how" | "/intro" | "/journal" | "/login" | "/onboarding" | "/pricing" | "/resources" | "/settings" | "/signup" | "/summary" | "/support" | "/support/announcements" | "/support/board" | "/support/contact" | "/support/faq";
		RouteParams(): {
			
		};
		LayoutParams(): {
			"/": Record<string, never>;
			"/business": Record<string, never>;
			"/chat": Record<string, never>;
			"/checkin": Record<string, never>;
			"/consent": Record<string, never>;
			"/download": Record<string, never>;
			"/features": Record<string, never>;
			"/goals": Record<string, never>;
			"/history": Record<string, never>;
			"/how": Record<string, never>;
			"/intro": Record<string, never>;
			"/journal": Record<string, never>;
			"/login": Record<string, never>;
			"/onboarding": Record<string, never>;
			"/pricing": Record<string, never>;
			"/resources": Record<string, never>;
			"/settings": Record<string, never>;
			"/signup": Record<string, never>;
			"/summary": Record<string, never>;
			"/support": Record<string, never>;
			"/support/announcements": Record<string, never>;
			"/support/board": Record<string, never>;
			"/support/contact": Record<string, never>;
			"/support/faq": Record<string, never>
		};
		Pathname(): "/" | "/business" | "/business/" | "/chat" | "/chat/" | "/checkin" | "/checkin/" | "/consent" | "/consent/" | "/download" | "/download/" | "/features" | "/features/" | "/goals" | "/goals/" | "/history" | "/history/" | "/how" | "/how/" | "/intro" | "/intro/" | "/journal" | "/journal/" | "/login" | "/login/" | "/onboarding" | "/onboarding/" | "/pricing" | "/pricing/" | "/resources" | "/resources/" | "/settings" | "/settings/" | "/signup" | "/signup/" | "/summary" | "/summary/" | "/support" | "/support/" | "/support/announcements" | "/support/announcements/" | "/support/board" | "/support/board/" | "/support/contact" | "/support/contact/" | "/support/faq" | "/support/faq/";
		ResolvedPathname(): `${"" | `/${string}`}${ReturnType<AppTypes['Pathname']>}`;
		Asset(): "/Gemini_Generated_Image_n90k8wn90k8wn90k-removebg-preview.png" | "/README.md" | string & {};
	}
}