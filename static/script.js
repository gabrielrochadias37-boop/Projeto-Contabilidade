// ================================
// SISTEMA DP & CONTABILIDADE - SCRIPT PRINCIPAL
// ================================

// Função para toggle de detalhes das contas
function toggledesc(codigo) {
  const row = document.getElementById("detalhe-" + codigo);
  const button = document.querySelector(`.btn-descricao-toggle[data-codigo="${codigo}"]`);
  
  if (!row || !button) return;

  const icon = button.querySelector("i");

  if (row.classList.contains("hidden")) {
    row.classList.remove("hidden");
    row.style.display = "table-row";
    if (icon) icon.className = "fas fa-chevron-up";
    button.innerHTML = '<i class="fas fa-chevron-up"></i> Ocultar';
  } else {
    row.classList.add("hidden");
    row.style.display = "none";
    if (icon) icon.className = "fas fa-chevron-down";
    button.innerHTML = '<i class="fas fa-chevron-down"></i> Detalhes';
  }
}

// Função para mudar cor do select de status
function mudarCor(select) {
  const valor = select.value;
  const cores = {
    'Pendente': '#a74128ff',
    'Feito': '#28a78cff', 
    'Fazendo': '#ffa620ff'
  };
  
  select.style.backgroundColor = cores[valor] || 'white';
  select.style.color = valor ? 'white' : 'black';
}

// Função para toggle de formulários CORRIGIDA
function toggleForm(id) {
  const div = document.getElementById(id);
  
  if (!div) {
    console.error('Elemento não encontrado:', id);
    return;
  }

  // Verifica se é um formulário de edição (tr element)
  const isTableRow = div.tagName.toLowerCase() === 'tr';
  
  // Encontra o ícone correspondente
  const icon = document.getElementById('toggle-icon-' + id);
  
  const isHidden = div.classList.contains('hidden') ||
                   div.style.display === 'none' ||
                   div.style.display === '';

  if (isHidden) {
    div.classList.remove('hidden');
    
    if (isTableRow) {
      div.style.display = 'table-row';
    } else {
      div.style.display = 'block';
    }
    
    if (icon) icon.textContent = '−';
    console.log(`Formulário ${id} expandido`);
  } else {
    div.classList.add('hidden');
    div.style.display = 'none';
    if (icon) icon.textContent = '+';
    console.log(`Formulário ${id} recolhido`);
  }
}

// Função específica para toggle de edição de contas
function toggleEditForm(formId) {
  console.log('Tentando alternar formulário:', formId);
  
  const formRow = document.getElementById(formId);
  if (!formRow) {
    console.error('Formulário de edição não encontrado:', formId);
    return;
  }

  const isHidden = formRow.classList.contains('hidden') || 
                   formRow.style.display === 'none' ||
                   formRow.style.display === '';

  if (isHidden) {
    // Primeiro fecha outros formulários de edição abertos
    document.querySelectorAll('tr[id^="editForm-"]').forEach(row => {
      if (row.id !== formId) {
        row.classList.add('hidden');
        row.style.display = 'none';
      }
    });

    // Abre o formulário atual
    formRow.classList.remove('hidden');
    formRow.style.display = 'table-row';
    console.log(`Formulário ${formId} aberto`);
  } else {
    // Fecha o formulário atual
    formRow.classList.add('hidden');
    formRow.style.display = 'none';
    console.log(`Formulário ${formId} fechado`);
  }
}

// Função para controlar campo ID Empresa
function toggleIdEmpresaField() {
  const tipoContaSelect = document.getElementById('tipo_conta');
  const idEmpresaInput = document.getElementById('idEmpresa');
  
  if (!tipoContaSelect || !idEmpresaInput) return;
  
  const tipoContaValue = tipoContaSelect.value;
  
  if (tipoContaValue === 'privada') {
    idEmpresaInput.disabled = false;
    idEmpresaInput.required = true;
    idEmpresaInput.placeholder = 'Digite o ID da empresa...';
  } else {
    idEmpresaInput.disabled = true;
    idEmpresaInput.required = false;
    idEmpresaInput.value = '';
    idEmpresaInput.placeholder = 'Disponível apenas para contas privadas';
  }
}

// Validação do formulário de contas
function validateContaForm(event) {
  const tipoContaSelect = document.getElementById('tipo_conta');
  const idEmpresaInput = document.getElementById('idEmpresa');
  
  if (!tipoContaSelect || !idEmpresaInput) return true;
  
  const tipoContaValue = tipoContaSelect.value;
  const idEmpresaValue = idEmpresaInput.value.trim();
  
  if (tipoContaValue === 'privada' && !idEmpresaValue) {
    event.preventDefault();
    alert('Para contas privadas, o ID da Empresa é obrigatório.');
    idEmpresaInput.focus();
    return false;
  }
  
  if (tipoContaValue === 'publica') {
    idEmpresaInput.value = '';
  }
  
  return true;
}

// ================================
// DASHBOARD - ANIMAÇÕES E CONTADORES
// ================================

// Função principal para animar contadores
function animateCounters() {
  console.log('🎬 Iniciando animação dos contadores...');
  
  const counters = document.querySelectorAll('.metric-value');
  
  if (counters.length === 0) {
    console.warn('⚠️ Nenhum contador encontrado para animar');
    return;
  }
  
  console.log(`📊 Encontrados ${counters.length} contadores para animar`);
  
  counters.forEach((counter, index) => {
    const originalText = counter.textContent.trim();
    console.log(`Contador ${index + 1}: "${originalText}"`);
    
    // Extrai o número do texto - suporte para percentuais
    let target = 0;
    let isPercentage = originalText.includes('%');
    
    if (isPercentage) {
      target = parseFloat(originalText.replace(/[^\d.]/g, '')) || 0;
    } else {
      target = parseInt(originalText.replace(/[^\d]/g, '')) || 0;
    }
    
    console.log(`Valor alvo: ${target}${isPercentage ? '%' : ''}`);
    
    // Define valor inicial
    counter.textContent = isPercentage ? '0%' : '0';
    
    if (target === 0) {
      // Se o alvo é 0, apenas define o valor final
      counter.textContent = isPercentage ? '0%' : '0';
      return;
    }
    
    // Configuração da animação
    const duration = 1500 + (index * 200); // Animações escalonadas
    const startTime = performance.now();

    function updateCounter(currentTime) {
      const elapsed = currentTime - startTime;
      const progress = Math.min(elapsed / duration, 1);
      
      // Efeito de easing suave
      const eased = progress < 0.5 
        ? 2 * progress * progress 
        : 1 - Math.pow(-2 * progress + 2, 2) / 2;
      
      const currentValue = Math.round(target * eased);
      
      // Atualiza o display
      if (isPercentage) {
        counter.textContent = `${currentValue}%`;
      } else {
        counter.textContent = currentValue.toLocaleString('pt-BR');
      }

      if (progress < 1) {
        requestAnimationFrame(updateCounter);
      } else {
        // Valor final exato
        counter.textContent = isPercentage 
          ? `${target}%` 
          : target.toLocaleString('pt-BR');
        
        console.log(`✅ Animação ${index + 1} concluída: ${counter.textContent}`);
      }
    }
    
    // Inicia a animação com delay
    setTimeout(() => {
      requestAnimationFrame(updateCounter);
    }, index * 100);
  });
}

// Função para atualizar data atual
function updateCurrentDate() {
  const dateEl = document.getElementById('current-date');
  if (dateEl) {
    const now = new Date();
    dateEl.textContent = now.toLocaleDateString('pt-BR', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
    console.log('📅 Data atualizada:', dateEl.textContent);
  }
}

// Função para inicializar dashboard
function initializeDashboard() {
  console.log('🚀 Inicializando dashboard...');
  
  const dashboardSection = document.getElementById('dashboard');
  if (!dashboardSection) {
    console.log('ℹ️ Dashboard não encontrado nesta página');
    return;
  }
  
  // Atualiza data
  updateCurrentDate();
  
  // Verifica se o dashboard está visível
  const isVisible = dashboardSection.offsetParent !== null && 
                   dashboardSection.style.display !== 'none';
  
  if (!isVisible) {
    console.log('ℹ️ Dashboard não está visível');
    return;
  }
  
  console.log('📊 Dashboard visível, iniciando animações...');
  
  // Múltiplas tentativas de animação para garantir sucesso
  const tryAnimate = (attempt = 1) => {
    const counters = document.querySelectorAll('.metric-value');
    
    if (counters.length > 0) {
      console.log(`✅ Tentativa ${attempt}: Encontrados ${counters.length} contadores`);
      animateCounters();
      return;
    }
    
    if (attempt < 5) {
      console.log(`⏳ Tentativa ${attempt}: Aguardando contadores... (${attempt * 300}ms)`);
      setTimeout(() => tryAnimate(attempt + 1), 300);
    } else {
      console.warn('⚠️ Contadores não encontrados após 5 tentativas');
    }
  };
  
  // Inicia as tentativas
  tryAnimate();
  
  // Adiciona interatividade aos cards
  document.querySelectorAll('.metric-card').forEach(card => {
    card.addEventListener('click', function() {
      const metric = this.dataset.metric;
      console.log(`📊 Card clicado: ${metric}`);
      
      // Adiciona efeito visual
      this.style.transform = 'scale(0.98)';
      setTimeout(() => {
        this.style.transform = 'scale(1)';
      }, 150);
    });
  });
}

// ================================
// INICIALIZAÇÃO ESPECÍFICA PARA CONTAS
// ================================

function initializeContasPage() {
  console.log('📊 Inicializando página de contas...');

  // 1. Inicializa contadores da página de contas
  const contadores = document.querySelectorAll('#contas .metric-value');
  if (contadores.length > 0) {
    console.log(`📊 Animando ${contadores.length} contadores da página de contas`);
    
    contadores.forEach((contador, index) => {
      const valor = parseInt(contador.textContent) || 0;
      let atual = 0;
      const incremento = valor / 30;
      contador.textContent = '0';
      
      const intervalo = setInterval(() => {
        atual += incremento;
        if (atual >= valor) {
          contador.textContent = valor;
          clearInterval(intervalo);
        } else {
          contador.textContent = Math.floor(atual);
        }
      }, 50);
    });
  }

  // 2. Garante que todos os formulários de edição começem ocultos
  document.querySelectorAll('tr[id^="editForm-"]').forEach(row => {
    row.classList.add('hidden');
    row.style.display = 'none';
  });

  console.log('✅ Página de contas inicializada!');
}

// ================================
// INICIALIZAÇÃO ESPECÍFICA PARA RELATÓRIOS
// ================================

function initializeRelatoriosPage() {
  console.log('📊 Inicializando página de relatórios...');

  const periodoSelect = document.getElementById('periodo');
  const mesGroup = document.getElementById('mesGroup');

  if (periodoSelect && mesGroup) {
    // Mostrar/ocultar campo de mês baseado na seleção do período
    periodoSelect.addEventListener('change', function() {
      if (this.value === 'personalizado') {
        mesGroup.style.display = 'flex';
      } else {
        mesGroup.style.display = 'none';
        document.getElementById('mes').value = '';
      }
    });

    // Reset form functionality
    const resetBtn = document.querySelector('button[type="reset"]');
    if (resetBtn) {
      resetBtn.addEventListener('click', function() {
        mesGroup.style.display = 'none';
      });
    }
  }

  console.log('✅ Página de relatórios inicializada!');
}

// ================================
// INICIALIZAÇÃO PRINCIPAL
// ================================

document.addEventListener('DOMContentLoaded', function() {
  console.log('🌟 Sistema DP & Contabilidade carregado!');
  
  // 1. Inicialização dos selects de status
  document.querySelectorAll('.statusSelect').forEach(select => {
    mudarCor(select);
    
    select.addEventListener('change', function() {
      mudarCor(this);
      console.log(`Status alterado: Conta ${this.dataset.conta} → ${this.value}`);
    });
  });
  
  // 2. Configuração de linhas ocultas
  document.querySelectorAll('tr.hidden').forEach(row => {
    row.style.display = 'none';
  });
  
  // 3. Botões de toggle de detalhes (para página de gerenciamento)
  document.querySelectorAll('.btn-descricao-toggle[data-codigo]').forEach(btn => {
    btn.addEventListener('click', function() {
      const codigo = this.getAttribute("data-codigo");
      toggledesc(codigo);
    });
  });
  
  // 4. Formulário de contas
  const tipoContaSelect = document.getElementById('tipo_conta');
  const contaForm = document.getElementById('contaForm');
  
  if (tipoContaSelect) {
    tipoContaSelect.addEventListener('change', toggleIdEmpresaField);
    toggleIdEmpresaField(); // Inicialização
  }
  
  if (contaForm) {
    contaForm.addEventListener('submit', validateContaForm);
  }
  
  // 5. Inicialização do Dashboard (se existir)
  initializeDashboard();
  
  // 6. Configura todos os botões de edição
  document.querySelectorAll('[data-toggle-edit]').forEach(btn => {
    const formId = btn.getAttribute('data-toggle-edit');
    btn.addEventListener('click', function(e) {
      e.preventDefault();
      toggleEditForm(formId);
    });
  });

  // 7. Configura botões de cancelar edição
  document.querySelectorAll('[data-cancel-edit]').forEach(btn => {
    const formId = btn.getAttribute('data-cancel-edit');
    btn.addEventListener('click', function(e) {
      e.preventDefault();
      toggleEditForm(formId); // vai fechar o form
    });
  });

  // 8. Inicialização específica da página de contas (se existir)
  const contasSection = document.getElementById('contas');
  if (contasSection) {
    initializeContasPage();
  }

  // 8.1. Inicialização específica da página de relatórios (se existir)
  const relatoriosSection = document.getElementById('relatorios');
  if (relatoriosSection) {
    initializeRelatoriosPage();
  }
  
  // 9. Botão de refresh (se existir)
  const refreshBtn = document.querySelector('button[onclick="location.reload()"]');
  if (refreshBtn) {
    refreshBtn.addEventListener('click', function(e) {
      e.preventDefault();
      console.log('🔄 Refresh solicitado');
      location.reload();
    });
  }
  
  console.log('✅ Inicialização completa!');
});

// ================================
// FUNÇÕES GLOBAIS PARA DEBUG
// ================================

// Expõe funções para debug no console
window.animateCounters = animateCounters;
window.updateCurrentDate = updateCurrentDate;
window.toggleEditForm = toggleEditForm;
window.toggleForm = toggleForm;
