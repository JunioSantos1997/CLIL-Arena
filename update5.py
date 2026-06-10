import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update HTML
html_old = """        <button class="btn-giant" id="btn-start">Start Challenge</button>
      </div>"""
html_new = """        <div style="display: flex; gap: 15px; justify-content: center; margin-top: 10px;">
          <button class="btn-giant" id="btn-start">Start Challenge</button>
          <button class="btn-reroll" id="btn-reroll" title="Reshuffle the deck">Reroll (<span id="reroll-count">3</span>)</button>
        </div>
      </div>"""
content = content.replace(html_old, html_new)

# 2. Update CSS
css_old = """    .btn-giant:hover {
      background: var(--bg-card);
      color: var(--gold);
    }"""
css_new = """    .btn-giant:hover {
      background: var(--bg-card);
      color: var(--gold);
    }
    
    .btn-reroll {
      font-family: var(--font-title);
      background: rgba(255, 255, 255, 0.1);
      color: var(--gold);
      border: 2px solid var(--gold);
      padding: 0 1.5rem;
      font-size: 1.2rem;
      cursor: pointer;
      clip-path: polygon(10px 0, 100% 0, 100% calc(100% - 10px), calc(100% - 10px) 100%, 0 100%, 0 10px);
      transition: all 0.2s;
      text-transform: uppercase;
      font-weight: bold;
      letter-spacing: 2px;
    }
    .btn-reroll:hover {
      background: rgba(212, 175, 55, 0.2);
    }
    .btn-reroll:disabled {
      opacity: 0.4;
      cursor: not-allowed;
      filter: grayscale(1);
    }"""
content = content.replace(css_old, css_new)

# 3. Add to state
state_old = """      pickedSpeakerIds: [],     // ID do membro sorteado como orador por equipe
      pickingSpeaker: []        // Bloqueia clique duplo durante animao
    };"""
state_new = """      pickedSpeakerIds: [],     // ID do membro sorteado como orador por equipe
      pickingSpeaker: [],       // Bloqueia clique duplo durante animao
      rerollsLeft: 3
    };"""
content = re.sub(r'pickedSpeakerIds:\s*\[\],\s*//.*\n\s*pickingSpeaker:\s*\[\]\s*//.*\n\s*\};', state_new, content)

# 4. Add to els
els_old = """      btnNext: $('#btn-next')
    };"""
els_new = """      btnNext: $('#btn-next'),
      btnReroll: $('#btn-reroll'),
      rerollCount: $('#reroll-count')
    };"""
content = content.replace(els_old, els_new)

# 5. Add event listener
event_old = """      els.btnNext.addEventListener('click', onNextRound);"""
event_new = """      els.btnNext.addEventListener('click', onNextRound);
      els.btnReroll.addEventListener('click', onReroll);"""
content = content.replace(event_old, event_new)

# 6. Add onReroll function before onStartChallenge
func_old = """    /* ----- FASE 2: Arena ----- */"""
func_new = """    /* ----- Reroll ----- */
    function onReroll() {
      if (state.rerollsLeft <= 0) return;
      
      state.rerollsLeft--;
      els.rerollCount.textContent = state.rerollsLeft;
      
      if (state.rerollsLeft === 0) {
        els.btnReroll.disabled = true;
      }

      // Hide revealed card
      els.revealedContainer.classList.remove('show');
      els.revealedImg.src = '';
      
      // Restore deck to trigger animation again
      els.deckWrapper.style.display = '';
      els.deckInstruction.style.display = '';
      els.deckWrapper.classList.remove('disabled');

      // Trigger the shuffle animation and random pick immediately
      onDeckClick();
    }

    /* ----- FASE 2: Arena ----- */"""
content = content.replace(func_old, func_new)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
