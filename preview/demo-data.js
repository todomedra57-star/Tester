// Sample view models for the preview: the four test cases from the design guide.
// Every key always exists; empty values mean "not filled in".

const photo = (seed, w = 600, h = 800) => {
  const hues = [[214, 222], [206, 230], [224, 248], [198, 216], [232, 210]][seed % 5];
  const mx = 30 + (seed * 37) % 45, my = 18 + (seed * 23) % 20;
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${w} ${h}">
<defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="hsl(${hues[0]} 38% 16%)"/><stop offset="1" stop-color="hsl(${hues[1]} 30% 42%)"/></linearGradient></defs>
<rect width="100%" height="100%" fill="url(#g)"/>
<circle cx="${mx}%" cy="${my}%" r="${w * 0.07}" fill="hsl(210 40% 90%)" opacity=".85"/>
<path d="M0 ${h * .78} Q ${w * .3} ${h * (.62 + seed % 3 * .04)} ${w * .55} ${h * .74} T ${w} ${h * .7} V ${h} H 0Z" fill="hsl(${hues[0]} 35% 10%)" opacity=".85"/>
<path d="M0 ${h * .88} Q ${w * .45} ${h * .8} ${w} ${h * .9} V ${h} H 0Z" fill="hsl(${hues[0]} 40% 6%)"/></svg>`;
  return 'data:image/svg+xml;utf8,' + encodeURIComponent(svg);
};

const MAP = 'https://maps.google.com/?q=';

export const CASES = {
  'demo-ar': {
    label: 'Demo wedding (Arabic)',
    lang: 'ar',
    vm: {
      verse: '﴿ وَمِنْ آيَاتِهِ أَنْ خَلَقَ لَكُم مِّنْ أَنفُسِكُمْ أَزْوَاجًا ﴾',
      couple: {
        groom: { name: 'أحمد محمود', father: 'الأستاذ/ محمود عبد الرحمن',
          family: [{ label: 'جد العريس', name: 'الحاج/ عبد الرحمن علي' }] },
        bride: { name: 'سارة خالد', father: 'المهندس/ خالد إبراهيم',
          family: [{ label: 'عم العروسة', name: 'الدكتور/ حسن إبراهيم' }] },
      },
      mainDate: '2027-02-12T20:00:00+03:00',
      story: {
        text: 'اتقابلنا أول مرة في فرح صحابنا، ومن ساعتها وإحنا بنكمل الحكاية سوا.',
        photos: [{ url: photo(1) }, { url: photo(2) }],
        engagementDate: '2026-03-20',
      },
      gallery: [0, 3, 4].map((s) => ({ url: photo(s), width: 600, height: 800 })),
      events: [
        { type: 'katb', date: '2027-02-11', time: 'بعد صلاة العشاء', venue: 'مسجد الحصري', area: '٦ أكتوبر',
          program: [], mapUrl: MAP + 'El+Hosary+Mosque' },
        { type: 'wedding', date: '2027-02-12', time: '20:00', venue: 'قاعة الماسة', area: 'مدينة نصر',
          program: [
            { time: '20:00', title: 'استقبال الضيوف' },
            { time: '20:30', title: 'زفة العروسين' },
            { time: '21:30', title: 'العشاء' },
          ], mapUrl: MAP + 'Nasr+City' },
      ],
      wishes: {
        presets: ['بارك الله لكما', 'ربنا يتمم بخير', 'ألف مبروك'],
        showOnPage: true, closeDate: '2027-02-19',
        approved: [{ name: 'خالة منى', text: 'ربنا يتمم بخير ويسعدكم' }],
      },
      closingLine: 'في انتظاركم لتكتمل فرحتنا',
      showBranding: true,
    },
  },

  'demo-en': {
    label: 'English invitation',
    lang: 'en',
    vm: {
      verse: '',
      couple: {
        groom: { name: 'Ahmed Mahmoud', father: 'Mr. Mahmoud Abdelrahman', family: [] },
        bride: { name: 'Sara Khaled', father: 'Eng. Khaled Ibrahim', family: [] },
      },
      mainDate: '2027-02-12T20:00:00+03:00',
      story: {
        text: 'We first met at our friends’ wedding, and we have been writing the story together ever since.',
        photos: [{ url: photo(1) }, { url: photo(2) }],
        engagementDate: '2026-03-20',
      },
      gallery: [0, 3, 4].map((s) => ({ url: photo(s), width: 600, height: 800 })),
      events: [
        { type: 'katb', date: '2027-02-11', time: 'After Isha prayer', venue: 'El Hosary Mosque', area: '6th of October',
          program: [], mapUrl: MAP + 'El+Hosary+Mosque' },
        { type: 'wedding', date: '2027-02-12', time: '20:00', venue: 'Al Masa Hall', area: 'Nasr City',
          program: [
            { time: '20:00', title: 'Guests arrive' },
            { time: '20:30', title: 'The zaffa' },
            { time: '21:30', title: 'Dinner' },
          ], mapUrl: MAP + 'Nasr+City' },
      ],
      wishes: {
        presets: ['Congratulations!', 'Wishing you a lifetime of joy', 'Mabrouk'],
        showOnPage: true, closeDate: '2027-02-19',
        approved: [{ name: 'Aunt Mona', text: 'May your home always be full of love.' }],
      },
      closingLine: 'We can’t wait to celebrate with you',
      showBranding: true,
    },
  },

  minimal: {
    label: 'Smallest invitation',
    lang: 'ar',
    vm: {
      verse: '',
      couple: { groom: { name: 'عمر', father: '', family: [] }, bride: { name: 'ليلى', father: '', family: [] } },
      mainDate: '2027-04-02T19:00:00+03:00',
      story: { text: '', photos: [], engagementDate: '' },
      gallery: [],
      events: [{ type: 'wedding', date: '2027-04-02', time: '19:00', venue: 'بيت العائلة', area: '', program: [], mapUrl: '' }],
      wishes: { presets: [], showOnPage: false, closeDate: '', approved: [] },
      closingLine: '',
      showBranding: false,
    },
  },

  longest: {
    label: 'Longest invitation',
    lang: 'ar',
    vm: {
      verse: '﴿ وَجَعَلَ بَيْنَكُم مَّوَدَّةً وَرَحْمَةً ﴾',
      couple: {
        groom: { name: 'عبد الرحمن محمد عبد العزيز عبد الله الشمري القحطاني',
          father: 'الأستاذ الدكتور/ محمد عبد العزيز عبد الله الشمري',
          family: ['جد العريس', 'عم العريس', 'خال العريس', 'عم العريس', 'خال العريس', 'أخو العريس']
            .map((label, i) => ({ label, name: `الأستاذ/ اسم طويل من العائلة رقم ${i + 1} الكريمة` })) },
        bride: { name: 'نورة عبد الله سلطان فهد العتيبي الدوسري الحربي',
          father: 'المهندس/ عبد الله سلطان فهد العتيبي',
          family: ['جد العروسة', 'عم العروسة', 'خال العروسة', 'عم العروسة', 'خال العروسة', 'أخو العروسة']
            .map((label, i) => ({ label, name: `الدكتور/ اسم طويل من العائلة رقم ${i + 1} الكريمة` })) },
      },
      mainDate: '2027-03-05T21:00:00+03:00',
      story: {
        text: 'حكايتنا بدأت من سنين طويلة في الجامعة، وكبرت مع كل يوم عشناه سوا، ومع كل حلم رسمناه لبيتنا. النهارده بنكمل أجمل فصل فيها، ومستنيين نشاركه معاكم.',
        photos: [{ url: photo(2) }, { url: photo(4) }],
        engagementDate: '2026-06-01',
      },
      gallery: [0, 1, 2, 3, 4].map((s) => ({ url: photo(s), width: 600, height: 800 })),
      events: ['katb', 'henna', 'engagement', 'wedding'].map((type, i) => ({
        type, date: `2027-03-0${2 + i}`, time: i % 2 ? 'بعد صلاة المغرب' : '21:00',
        venue: 'قاعة الأمير للاحتفالات والمناسبات الكبرى الملحقة بفندق الواحة الدولي',
        area: 'حي الملقا، شمال مدينة الرياض',
        program: i === 3 ? [
          { time: '21:00', title: 'استقبال الضيوف' }, { time: '22:00', title: 'دخول العريس' },
          { time: '23:00', title: 'العشاء' }, { time: '00:30', title: 'زفة العروس' },
        ] : [],
        mapUrl: MAP + 'Riyadh',
      })),
      wishes: {
        presets: ['بارك الله لكما وبارك عليكما', 'ألف مبروك', 'ربنا يتمم بخير', 'بالرفاء والبنين'],
        showOnPage: true, closeDate: '2027-03-12',
        approved: [
          { name: 'أم فهد', text: 'بارك الله لكما وجمع بينكما في خير' },
          { name: 'صديق العائلة', text: 'ألف ألف مبروك، ربنا يسعدكم' },
        ],
      },
      closingLine: 'حضوركم يكمّل فرحتنا، وننتظركم بكل الحب والشوق',
      showBranding: true,
    },
  },
};
