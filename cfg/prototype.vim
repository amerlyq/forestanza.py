" Opts -- don't work: au! in local .vimrc is disabled by 'set exrc secure'
" set wrap

fun! AddLexicGroup(nm, clr, items)
    exec 'hi! '. a:nm .' ctermbg=None guibg=None ctermfg='. a:clr
    let l:lst = []
        if type("") == type(a:items) | let l:lst=[a:items]
    elseif type([]) == type(a:items) | let l:lst=a:items
    elseif type({}) == type(a:items) | let l:lst=extend(keys(a:items), values(a:items))
    endif
    call matchadd(a:nm, '\v\c'. join(l:lst, '|'), -1)
endfunction

" Maps
noremap ga :Tabularize /<bar>\<bar>:\<bar>>/l1l1r1c1l1<CR>
noremap g; 0f:<Left>
noremap g\ 0f<bar><Right>

""" Legend """
